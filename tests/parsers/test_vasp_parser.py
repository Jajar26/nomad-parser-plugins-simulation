import pytest
from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.datamodel.context import ServerContext
from nomad.files import StagingUploadFiles
from nomad.processing import Upload
from nomad.utils import get_logger

from nomad_simulation_parsers.parsers.vasp.parser import VASPParser

LOGGER = get_logger(__name__)

@pytest.fixture
def test_upload_files():
    return StagingUploadFiles(upload_id='test_upload', create=True)

@pytest.fixture
def test_upload(test_upload_files):
    upload = Upload(upload_id='test_upload')
    # test_upload_files.add_rawfiles('external.h5')
    return upload


@pytest.fixture
def test_context(test_upload):
    return ServerContext(upload=test_upload)


@pytest.fixture(scope='function')
def parser():
    return VASPParser()

def test_vasprun(parser):
    archive = EntryArchive()
    parser.parse('tests/data/vasp/AgAc_relax/vasprun.xml.relax', archive, LOGGER)


def test_outcar(parser):
    archive = EntryArchive()
    parser.parse('tests/data/vasp/AgAc_relax/OUTCAR', archive, LOGGER)


@pytest.mark.skip(reason='Lift once fix is merged in nomad-lab')
def test_chgcar(parser, test_context, test_upload):
    archive = EntryArchive(
        m_context=test_context,
        metadata=EntryMetadata(upload_id=test_upload.upload_id, entry_id='test_entry')
    )
    parser.parse('tests/data/vasp/with_chgcar/OUTCAR', archive, LOGGER)
