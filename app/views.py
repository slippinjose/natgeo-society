import logging
import os

from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='templates')

log = logging.getLogger(__name__)


@home_bp.route('/planetary')
def planetary():
    return render_template('planetary.html')

@home_bp.route('/google_maps')
def gmaps():
    return render_template('gmaps.html')

@home_bp.route('/mapbox')
def mapbox():
    return render_template('mapbox.html', mapbox_token=os.environ.get('MAPBOX_API_KEY'))
