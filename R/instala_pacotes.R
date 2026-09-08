# Instala, dentro do próprio pacote, o que a etapa 05 precisa.
# Rode uma vez se .tools/R-library estiver ausente ou incompleta:
#   Rscript R/instala_pacotes.R
lib <- file.path(getwd(), '.tools', 'R-library')
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, .libPaths()))
necessarios <- c('fixest', 'data.table', 'jsonlite')
faltando <- necessarios[!necessarios %in% rownames(installed.packages())]
if (length(faltando)) {
  install.packages(faltando, lib = lib, repos = 'https://cloud.r-project.org')
} else {
  cat('Nada a instalar.\n')
}
for (p in necessarios) cat(p, as.character(packageVersion(p)), '\n')
