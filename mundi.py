import click
from core import capture_from_url, set_topic, list_topics, topic as current_topic
from utilities import safe_filename


@click.group()
def main():
    pass


@main.group(invoke_without_command=True)
def topic():
    """Commands related to topics. Without a subcommand, show the current topic."""
    click.echo(current_topic())


@topic.command()
def list():
    """List available topics."""
    click.echo(
        "\n".join(list_topics())
)


@main.command()
@click.argument("url")
def save(url):
    saved = capture_from_url(url)
    click.echo(f'saved to {saved}')
    

@topic.command()
@click.argument('topic')
def set(topic):
    """Set the topic."""
    topic = safe_filename(topic)
    output = set_topic(topic)
    click.echo(f"Topic set to {output}")
    
              

if __name__ == '__main__':
    main()
