"""
viewerJS.py
-------------

Render trimesh.Scene objects using three.js
"""
import os
import json
import base64

# for our template
from ..resources import get_resource


def scene_to_html(scene):
    """
    Return HTML that will render the scene.
    Uses GLTF/GLB encoded to base64.

    Parameters
    --------------
    scene: trimesh.Scene object

    Returns
    --------------
    html: str, HTML containing embedded geometry
    """
    # use os.path.join so this works on windows
    base = get_resource('viewer.html.template')

    # get export as bytes
    data = scene.export(file_type='glb')
    # encode as base64 string
    encoded = base64.b64encode(data).decode('utf-8')

    # replace keyword with our scene data
    result = base.replace('$B64GLTF', encoded)

    return result


def scene_to_notebook(scene, height=600):
    """
    Convert a scene to HTML containing embedded geometry
    and a three.js viewer that will display nicely in
    an IPython/Jupyter notebook.

    Parameters
    -------------
    scene: trimesh.Scene object

    Returns
    -------------
    html: IPython.display.HTML object
    """
    # keep as soft dependency
    from IPython import display

    # convert scene to a full HTML page
    as_html = scene_to_html(scene=scene)

    # escape the quotes in the HTML
    srcdoc = as_html.replace('"', '&quot;')
    # embed this puppy as the srcdoc attr of an IFframe
    # I tried this a dozen ways and this is the only one that works
    # display.HTML and display.Javascript really, really don't work
    embeded = display.HTML('<iframe srcdoc="{srcdoc}" '
                           'width="100%" height="{height}px" '
                           'style="border:none;"></iframe>'.format(
                               srcdoc=srcdoc,
                               height=height))
    return embeded


def in_notebook():
    """
    Check to see if we are in an IPython or Jypyter notebook.

    Returns
    -----------
    in_notebook: bool, True if we are in a notebook
    """
    try:
        # function returns ipython context
        ipy = get_ipython()
        # we only want to render rich output in notebooks
        # in terminals we definitly do not want to output HTML
        terminal = 'terminal' in ipy.__class__.__name__.lower()
        return not terminal

    except BaseException:
        return False
