# main.py

import argparse
import re
from pathlib import Path

import pymupdf
from rich import print
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.prompt import Prompt


def collect_files(
    list_of_paths: list[Path], filter: list[str] = [".pdf"]
) -> list[Path]:
    files = list()
    for f in list_of_paths:
        if f.is_file() and f.suffix in filter:
            files.append(f)
        elif f.is_dir():
            [files.append(p) for p in f.rglob("*") if p.suffix in filter]
    return files


parser = argparse.ArgumentParser(
    prog="PDF Watermark Remover",
    description="Removes specific watermarks losslessly from PDF files.",
    epilog="Happy cleaning!",
)
parser.add_argument("files", nargs="*", help="Paths of files and folders", type=Path)
parser.add_argument("-t", "--text", help="Exact text to remove", type=str)
parser.add_argument(
    "-p", "--pattern", help="Advanced: Regex pattern to remove dynamic text", type=str
)
args = parser.parse_args()


def remove_watermark_text(
    input_path: Path, search_pattern: re.Pattern, progress: Progress
):
    doc = pymupdf.open(input_path)

    task_id = progress.add_task(f"[cyan]Scanning {input_path.name}...", total=len(doc))

    for page in doc:
        text = str(page.get_text())
        matches = search_pattern.findall(text)

        if matches:
            for match in set(matches):
                text_instances = page.search_for(match)

                for inst in text_instances:
                    page.add_redact_annot(inst)

            try:
                page.apply_redactions(images=False, graphics=False)

            except Exception as e:
                for match in set(matches):
                    for inst in page.search_for(match):
                        rect = inst + (-2, -2, 2, 2)
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))

        progress.advance(task_id)

    progress.update(task_id, description=f"[green]Saving {input_path.name}...")

    output_path = input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")
    doc.save(output_path, garbage=4, deflate=True)

    progress.update(task_id, description=f"[bold green]Done {input_path.name}")


def get_pattern() -> re.Pattern:

    if args.text:
        search_pattern = re.compile(re.escape(args.text), re.DOTALL)
        print(f"[cyan]Using exact text search:[cyan] {args.text}\n")
    elif args.pattern:
        search_pattern = re.compile(args.pattern, re.DOTALL)
        print(f"[cyan]Using custom Regex pattern:[cyan] {args.pattern}\n")
    else:
        print("[bold yellow]What watermark would you like to remove?[/bold yellow]")
        print(" [1] Default pattern (Tack för att du köpt... + dynamic order numbers)")
        print(" [2] Enter exact text to remove manually")
        print(" [3] Enter a custom Regex pattern")

        choice = Prompt.ask("\nChoose an option", choices=["1", "2", "3"], default="1")
        print()

        if choice == "1":
            search_pattern = re.compile(
                r"Tack för att du köpt den här boken! Order:.*?(?:förbjuden\.?)",
                re.DOTALL,
            )
        elif choice == "2":
            user_text = Prompt.ask(
                "[bold cyan]Enter the exact text to remove[/bold cyan]"
            )
            search_pattern = re.compile(re.escape(user_text), re.DOTALL)
            print()
        else:
            user_pattern = Prompt.ask("[bold cyan]Enter your Regex pattern[/bold cyan]")
            search_pattern = re.compile(user_pattern, re.DOTALL)
            print()

    return search_pattern


def main() -> None:
    print("[bold chartreuse3]PDF Cleaner script started[/bold chartreuse3]\n")
    files = collect_files(args.files)

    if not files:
        print("[bold red]No valid files were imported[/bold red]")
        exit(1)
    else:
        print("[bold purple]Files imported:[/bold purple]")
        for file in files:
            print(f"[deep_sky_blue1] - {file.name}")
        print()

    search_pattern = get_pattern()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    ) as progress:

        overall_task = progress.add_task(
            "[bold purple]Overall Progress...", total=len(files)
        )

        for file in files:
            remove_watermark_text(file, search_pattern, progress)
            progress.advance(overall_task)

    print("\n[bold chartreuse3]All files processed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("\n[bold yellow]Script was aborted by user...")
