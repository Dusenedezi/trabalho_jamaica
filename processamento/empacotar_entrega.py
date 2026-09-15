"""Empacota o repositório para entrega ao professor.

Cria <sobrenome>_jamaica_AM1.zip na pasta acima do repositório (ou em --saida), com a
pasta renomeada dentro do zip, sem .venv/, .git/, __pycache__/ e arquivos temporários.
Nada no repositório é alterado. Rode depois de converter uso_de_ia_AM1 para PDF.

Uso:  python processamento/empacotar_entrega.py [--sobrenome senedese] [--saida PASTA]
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EXCLUIR_DIRS = {".venv", ".git", "__pycache__", ".pytest_cache", ".idea", ".vscode"}
EXCLUIR_EXT = {".pyc", ".tmp"}
ESPERADOS = ["README.md", "requirements.txt", "config/series.yaml", "processamento/run_all.py",
             "dados/processados/fontes.csv", "dados/processados/log_extracao.csv",
             "dados/processados/verificacao.txt", "uso_de_ia_AM1.md", "uso_de_ia_AM1.pdf"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sobrenome", default="senedese")
    ap.add_argument("--saida", default=str(RAIZ.parent))
    a = ap.parse_args()

    faltando = [e for e in ESPERADOS if not (RAIZ / e).exists()]
    if faltando:
        print("AVISO: arquivos esperados ausentes:", ", ".join(faltando))

    nome = f"{a.sobrenome}_jamaica_AM1"
    zpath = Path(a.saida) / f"{nome}.zip"
    n, total = 0, 0
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(RAIZ.rglob("*")):
            rel = p.relative_to(RAIZ)
            if p.is_dir() or any(part in EXCLUIR_DIRS for part in rel.parts) or p.suffix in EXCLUIR_EXT:
                continue
            z.write(p, f"{nome}/{rel.as_posix()}")
            n += 1
            total += p.stat().st_size
    print(f"{zpath}\n  {n} arquivos, {total / 1e6:.1f} MB antes da compressão, {zpath.stat().st_size / 1e6:.1f} MB no zip")
    with zipfile.ZipFile(zpath) as z:
        pastas = sorted({Path(i).parts[1] for i in z.namelist() if len(Path(i).parts) > 2})
        print("  pastas incluídas:", ", ".join(pastas))
        assert not any(".venv" in i or "__pycache__" in i for i in z.namelist()), "zip contém .venv ou __pycache__"


if __name__ == "__main__":
    main()
