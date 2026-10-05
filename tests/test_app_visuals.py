"""Local illustration, accessible guidance and data-derived resource context."""

from pathlib import Path
import socket
import xml.etree.ElementTree as ET

from streamlit.testing.v1 import AppTest

from vayu.quality import read_pack


ROOT = Path(__file__).resolve().parents[1]


def test_header_and_workflow_render_without_outbound_connections(tmp_path, monkeypatch):
    """The visual app must work from local assets with network access prohibited."""
    original_connect = socket.socket.connect
    original_connection = socket.create_connection
    loopback = {'127.0.0.1', '::1', 'localhost'}

    def connect(sock, address):
        if isinstance(address, tuple) and address[0] in loopback:
            return original_connect(sock, address)  # Windows asyncio socket-pair.
        raise AssertionError('The visual presentation cannot open outbound connections')

    def connection(address, *args, **kwargs):
        if address[0] in loopback:
            return original_connection(address, *args, **kwargs)
        raise AssertionError('The visual presentation cannot open outbound connections')

    monkeypatch.setattr(socket.socket, 'connect', connect)
    monkeypatch.setattr(socket, 'create_connection', connection)
    monkeypatch.setenv('VAYU_DB_PATH', str(tmp_path / 'visuals.db'))
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=20).run()
    assert not app.exception
    images = [image for node in app.get('image') for image in node.proto.imgs]
    assert any('Fictional aircraft' in image.alt for image in images)
    assert any('Check data' in image.alt and 'review' in image.alt for image in images)
    assert all(image.alt and not image.url.startswith(('http://', 'https://')) for image in images)
    assert any('Concept illustration' in item.value for item in app.caption)
    assert any('How to use this prototype' == item.label for item in app.expander)
    state = read_pack(ROOT / 'data/whatif_demo', safety_buffer=0).state
    metrics = {item.label: item.value for item in app.metric}
    assert int(metrics['Maintenance bays']) == len(state.bays)
    assert int(metrics['Technician crews']) == len(state.crews)
    assert int(metrics['Spare engines in pack']) == len(state.spares)


def test_visual_assets_are_portable_and_have_no_external_content():
    """Ship compact, valid graphics without scripts or remote font/image URLs."""
    assets = ROOT / 'ui/assets'
    assert (assets / 'hangar.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    for path in assets.glob('*'):
        assert path.stat().st_size < 5 * 1024 * 1024
    for name in ('wordmark.svg', 'workflow.svg'):
        graphic = ET.fromstring((assets / name).read_bytes())
        assert graphic.tag.endswith('svg')
        assert graphic.find('{http://www.w3.org/2000/svg}title') is not None
        for element in graphic.iter():
            assert not element.tag.endswith('script')
            for attribute, value in element.attrib.items():
                if attribute.endswith(('href', 'src')):
                    assert not value.startswith(('http:', 'https:', '//'))
    provenance = (assets / 'README.md').read_text(encoding='utf-8')
    assert 'concept illustration' in provenance.lower() and 'Prompt' in provenance
