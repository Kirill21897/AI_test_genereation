"""
CLI-интерфейс для LLM-core
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from dotenv import load_dotenv
from core.models import GenerationInput
from core.generator import TestGenerator
import json
from datetime import datetime

load_dotenv(override=True)

app = typer.Typer(help="LLM-core — генератор тестов для нефтегазовой отрасли")
console = Console()

@app.callback()
def main() -> None:
    """Корневая CLI-группа для команд генератора."""
    pass

@app.command()
def generate(
    topic: str = typer.Option(..., "--topic", "-t", help="Тема теста, например: 'Контроль скважины'"),
    specialty: str = typer.Option(..., "--specialty", "-s", help="Специальность, например: 'Инженер по бурению'"),
    level: str = typer.Option("Senior", "--level", "-l", help="Уровень: Junior, Middle, Senior, Expert"),
    num_questions: int = typer.Option(5, "--num", "-n", help="Количество вопросов", min=3, max=15),
    output: str = typer.Option(None, "--output", "-o", help="Сохранить результат в JSON-файл"),
):
    """
    Генерирует тест по заданным параметрам.
    """
    try:
        console.print(Panel.fit(
            f"[bold blue]Генерация теста[/bold blue]\n"
            f"Тема: [cyan]{topic}[/cyan]\n"
            f"Специальность: [cyan]{specialty}[/cyan]\n"
            f"Уровень: [cyan]{level}[/cyan] | Вопросов: [cyan]{num_questions}[/cyan]",
            title="LLM-core"
        ))

        # Подготовка входных данных
        input_data = GenerationInput(
            topic=topic,
            specialty=specialty,
            level=level,
            num_questions=num_questions,
        )

        # Генерация теста
        generator = TestGenerator()
        test = generator.generate(input_data)

        # Вывод результата
        rprint(f"\n[bold green]✅ Тест успешно сгенерирован![/bold green] (ID: {test.test_id})")
        rprint(f"Название: [bold]{test.title}[/bold]")
        rprint(f"Вопросов: {len(test.questions)} | Judge Score: {test.metadata.get('judge_score', 'N/A')}\n")

        # Показываем первые 2 вопроса в консоли
        for i, q in enumerate(test.questions[:2], 1):
            console.print(Panel(
                f"[bold]Вопрос {i}:[/bold] {q.question_text[:300]}...\n\n"
                f"[dim]Тип: {q.type} | Сложность: {q.difficulty} | Bloom: {q.bloom_level}[/dim]",
                title=f"Пример вопроса {i}",
                border_style="blue"
            ))

        # Сохранение в файл
        if output:
            filename = output if output.endswith(".json") else f"{output}.json"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(test.model_dump_json(indent=2))
            rprint(f"[green]Тест сохранён в файл:[/green] {filename}")

        return test

    except Exception as e:
        console.print(f"[bold red]Ошибка:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
