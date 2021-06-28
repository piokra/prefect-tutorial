from models.av_models import InterdayResponseModel
from resources.interday_15m_example import INTERDAY_15M_IBM_DICT


def test_model_parses_example_av_api_response():
    assert InterdayResponseModel.parse_obj(INTERDAY_15M_IBM_DICT)
