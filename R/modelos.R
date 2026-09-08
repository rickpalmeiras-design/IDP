# Estimação dos modelos de probabilidade linear com efeitos fixos de alta dimensão.
# Chamado pela etapa 05 com um JSON de job; nada aqui lê config.yaml diretamente.
.libPaths(c(file.path(getwd(), '.tools', 'R-library'), .libPaths()))
suppressPackageStartupMessages(library(fixest))
suppressPackageStartupMessages(library(data.table))
library(jsonlite)

j <- fromJSON(commandArgs(TRUE)[1], simplifyVector = FALSE)
set.seed(j$seed); setFixest_nthreads(j$threads); setDTthreads(j$threads)
d <- fread(j$dados, na.strings = c('', 'NA', 'NaN'))
if ('pos' %in% names(d)) d[, pos := as.numeric(as.logical(pos))]

# Categorias ausentes viram uma categoria própria: a célula não é descartada em silêncio.
categoricas <- c('sexo', 'raca', 'escolaridade', 'tempo_emprego_categoria',
                 'tamanho_empresa_categoria', 'setor')
for (v in intersect(categoricas, names(d))) {
  d[, (v) := as.character(get(v))]
  d[is.na(get(v)), (v) := 'ignorado']
  d[, (v) := as.factor(get(v))]
}

for (i in seq_along(j$modelos)) {
  item <- j$modelos[[i]]
  name <- paste0(j$nome, '_', item$nome)
  cat('\nEstimando', name, '\n'); flush.console()
  args <- list(fml = as.formula(item$formula), data = d,
               vcov = as.formula(paste('~', j$cluster)), mem.clean = TRUE, notes = TRUE)
  if (!is.null(j$pesos)) args$weights <- as.formula(paste('~', j$pesos))
  m <- do.call(feols, args)

  v <- vcov(m); ct <- as.data.frame(coeftable(m))
  out <- data.frame(termo = rownames(ct), estimativa = ct[, 1], erro_padrao = ct[, 2],
                    estatistica = ct[, 3], p_valor = ct[, 4], n = nobs(m), modelo = name)

  # Inferência conservadora: graus de liberdade pelo número de clusters efetivamente usados.
  used_obs <- fixest::obs(m)
  df_cluster <- length(unique(d[[j$cluster]][used_obs])) - 1
  out$erro_padrao_conservador <- out$erro_padrao
  out$graus_liberdade_conservador <- df_cluster
  out$p_valor_conservador <- 2 * pt(-abs(out$estimativa / out$erro_padrao_conservador), df = df_cluster)
  out$ic95_inferior_conservador <- out$estimativa - qt(.975, df_cluster) * out$erro_padrao_conservador
  out$ic95_superior_conservador <- out$estimativa + qt(.975, df_cluster) * out$erro_padrao_conservador

  write.csv(out, file.path(j$output, paste0(name, '.csv')), row.names = FALSE)
  write.csv(v, file.path(j$output, paste0(name, '_vcov.csv')))
  write_json(list(formula = item$formula, n = nobs(m), cluster = j$cluster, pesos = j$pesos,
                  clusters = df_cluster + 1, pacote = as.character(packageVersion('fixest')),
                  observacoes_entrada = nrow(d), sha256_dados = j$sha256_dados),
             file.path(j$output, paste0(name, '_metadados.json')), auto_unbox = TRUE, pretty = TRUE)
  rm(m); gc()
}
