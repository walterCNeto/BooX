# BooX — imagem isolada para rodar o framework sem rede
#
# Build:
#   docker build -t boox:0.2.1 .
#
# Run (monta pasta da instancia em /data):
#   docker run --rm --network=none -v %cd%\examples\banco_modelo_sa:/data boox:0.2.1
#
# A flag --network=none garante isolamento total. O BooX nao precisa de rede,
# e esta e a prova para a SI.
FROM python:3.12-slim

LABEL org.opencontainers.image.title="BooX"
LABEL org.opencontainers.image.description="Framework de risco operacional — rodar com --network=none"
LABEL org.opencontainers.image.source="https://github.com/walterCNeto/BooX"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY pyproject.toml README.md LICENSE SECURITY.md ./
COPY boox ./boox
COPY canonico ./canonico
COPY schema ./schema

# openpyxl so e instalado se os templates forem necessarios
# por padrao, imagem minima sem dependencias externas
RUN pip install --no-cache-dir .

VOLUME ["/data", "/out"]
WORKDIR /data

# Entrypoint padrao: rodar o 20-box com --air-gapped (defesa em profundidade,
# somada ao --network=none do runtime)
ENTRYPOINT ["python", "-m", "boox"]
CMD ["/data", "--out", "/out", "--air-gapped"]
