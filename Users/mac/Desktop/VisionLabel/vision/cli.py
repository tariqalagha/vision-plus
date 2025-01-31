import click
import asyncio
from .main import VisionPlus

@click.group()
def cli():
    """Vision Plus CLI"""
    pass

@cli.command()
@click.option('--config', '-c', help='Path to config file')
def start(config):
    """Start Vision Plus server"""
    asyncio.run(VisionPlus(config).start())

@cli.command()
def status():
    """Check system status"""
    click.echo("Checking Vision Plus status...")