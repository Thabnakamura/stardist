import pytest
import numpy as np
from stardist.models import StarDist2D, StarDist3D
from stardist.data import test_image_nuclei_2d as _test_image_2d
from stardist.data import test_image_nuclei_3d as _test_image_3d

from stardist.bioimageio_utils import export_bioimageio, _import
missing = _import(error=False) is None
if not missing:
    from bioimageio.core.resource_tests import test_model as _test_model


def _test_pretrained(tmp_path, model_name, test_image, model_type=StarDist2D):
    model = model_type.from_pretrained(model_name)
    assert model is not None
    out_path = tmp_path / f"{model_name}.zip"
    export_bioimageio(model, out_path, test_input=test_image)
    assert out_path.exists()
    res = _test_model(out_path)
    # breakpoint()
    assert not res["error"]


@pytest.mark.skipif(missing, reason="Requires bioimageio dependencies")
def test_pretrained_fluo(tmp_path):
    test_image = _test_image_2d()
    model_name = "2D_versatile_fluo"
    _test_pretrained(tmp_path, model_name, test_image)


# @pytest.mark.skipif(missing, reason="Requires bioimageio dependencies")
# def test_pretrained_paper(tmp_path):
#     test_image = _test_image_2d()
#     model_name = "2D_paper_dsb2018"
#     _test_pretrained(tmp_path, model_name, test_image)


@pytest.mark.skipif(missing, reason="Requires bioimageio dependencies")
def test_pretrained_he(tmp_path):
    test_image = _test_image_2d()
    test_image = np.concatenate([test_image[..., None]] * 3, axis=-1)
    model_name = "2D_versatile_he"
    _test_pretrained(tmp_path, model_name, test_image)


@pytest.mark.skipif(missing, reason="Requires bioimageio dependencies")
def test_pretrained_3d(tmp_path):
    test_image = _test_image_3d()
    model_name = "3D_demo"
    _test_pretrained(tmp_path, model_name, test_image, model_type=StarDist3D)
