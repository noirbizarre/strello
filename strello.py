import json
import csv

import click


def color(name, **kwargs):
    return lambda t: click.style(str(t), fg=name, **kwargs)

green = color('green', bold=True)
yellow = color('yellow', bold=True)
red = color('red', bold=True)
cyan = color('cyan')
magenta = color('magenta', bold=True)
white = color('white', bold=True)
echo = click.echo

ARROW = '⇢'

CSV_FORMAT = {
    'delimiter': ';',
    'quotechar': '"',
    'quoting': csv.QUOTE_NONNUMERIC,
    'lineterminator': '\n',
}


def arrow(msg):
    echo('{0} {1}'.format(yellow(ARROW), msg))


def label_arrow(label, msg):
    arrow('{0}: {1}'.format(white(label), msg))


def indent(msg):
    echo('\t{0}'.format(msg))


@click.command()
@click.argument('dump', required=True, type=click.File('r'))
@click.option('-o', '--output', required=False, type=click.File('w'))
@click.option('-v', '--verbose', is_flag=True)
def cli(dump, output, verbose):
    '''Extract some statistics from Trello JSON dump'''
    filename = dump.name
    label_arrow('Filename', filename)
    data = json.load(dump)
    label_arrow('Name', data['name'])
    label_arrow('Extracted on', data['dateLastView'])
    label_arrow('URL', data['url'])
    label_arrow('Short URL', data['shortLink'])
    if output:
        label_arrow('CSV output', output.name)
    arrow('{0} lists'.format(len(data['lists'])))

    # Store lists for quick access by ID
    lists = {}
    ordered_lists = sorted(data['lists'], key=lambda k: k['pos'])
    for lst in ordered_lists:
        if verbose:
            cards = [c for c in data['cards'] if c['idList'] == lst['id']]
            indent('{name} ({status}): {nb} cards'.format(
                name=white(lst['name']),
                nb=len(cards),
                status=red('closed') if lst['closed'] else green('open')
            ))
        lists[lst['id']] = lst

    arrow('{0} cards'.format(len(data['cards'])))
    if output:
        header = ['name', 'id', 'url', 'created', 'closed', 'due', 'labels', 'list']
        header.extend(l['name'] for l in ordered_lists)
        w = csv.writer(output, **CSV_FORMAT)
        w.writerow(header)
    for card in data['cards']:
        if verbose:
            indent('{name} ({status}): {list}'.format(
                name=white(card['name']),
                list=lists[card['idList']]['name'],
                status=red('closed') if card['closed'] else green('open')
            ))
        if output:
            actions = get_actions_for_card(card, data)
            w.writerow([
                card['name'],
                card['id'],
                card['shortUrl'],
                get_creation_date(card, actions),
                card['closed'],  # Get the date
                card['due'],
                ','.join(l['name'] for l in card['labels']),
                lists[card['idList']]['name'],
            ] + [
                get_list_date(card, actions, lst)
                for lst in ordered_lists
            ])

    # print('data keys', data.keys())
    # print('list keys', data['lists'][0].keys())
    # print('card keys', data['cards'][0].keys())
    # print('action keys', data['actions'][0].keys())


def get_actions_for_card(card, data):
    return [
        a for a in data['actions']
        if 'card' in a['data'] and a['data']['card']['id'] == card['id']
    ]


def get_creation_date(card, actions):
    actions = [a for a in actions if a['type'] == 'createCard']
    if not actions:
        return
    return actions[0]['date']


def get_list_date(card, actions, lst):
    dates = [
        a['date'] for a in actions
        if (
            (a['type'] == 'createCard' and a['data']['list']['id'] == lst['id']) or
            (a['type'] == 'updateCard' and a['data'].get('listAfter', {}).get('id') == lst['id'])
        )
    ]
    if not dates:
        return
    return sorted(dates)[-1]
