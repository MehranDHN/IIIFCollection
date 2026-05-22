import argparse
import shutil
import subprocess
from pathlib import Path


def generate_dot(dot_path: Path) -> None:
    subprocess.run(
        [
            'python',
            str(Path(__file__).resolve().parent / 'generate_persons_graph_dot.py'),
        ],
        check=True,
    )
    if not dot_path.exists():
        raise FileNotFoundError(f'Expected DOT file not found: {dot_path}')


def render_dot(dot_path: Path, output_path: Path, output_format: str) -> None:
    dot_exe = shutil.which('dot')
    if not dot_exe:
        raise FileNotFoundError(
            'Graphviz `dot` executable not found. Install Graphviz or add it to PATH.'
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [dot_exe, f'-T{output_format}', str(dot_path), '-o', str(output_path)],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate Persons TTL DOT and optional SVG/PNG output.'
    )
    parser.add_argument(
        '--format',
        choices=['svg', 'png'],
        default='svg',
        help='Output format to render from DOT.',
    )
    parser.add_argument(
        '--dot',
        default='persons_graph.dot',
        help='DOT file path to generate or render.',
    )
    parser.add_argument(
        '--output',
        help='Rendered output file path. Defaults to persons_graph.<format>.',
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    dot_path = script_dir / args.dot
    output_path = (
        script_dir / args.output
        if args.output
        else script_dir / f'persons_graph.{args.format}'
    )

    print('Generating DOT file...')
    generate_dot(dot_path)
    print(f'Generated DOT: {dot_path}')

    print(f'Rendering {args.format.upper()} output...')
    render_dot(dot_path, output_path, args.format)
    print(f'Rendered {output_path}')


if __name__ == '__main__':
    main()
