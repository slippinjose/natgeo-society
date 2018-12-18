import logging
import os

from flask import Blueprint, render_template

from app.handlers import UnbabelitesHandler

home_bp = Blueprint('home', __name__, template_folder='templates')

log = logging.getLogger(__name__)


@home_bp.route('/planetary')
def planetary():
    unbabelites = UnbabelitesHandler.get_all()

    return render_template('planetary.html')

@home_bp.route('/google_maps')
def gmaps():
    unbabelites = UnbabelitesHandler.get_all()

    return render_template('gmaps.html', 
                           unbabelites=unbabelites.raw,
                           google_maps_api_key=os.environ.get('GOOGLE_MAPS_API_KEY'))

@home_bp.route('/mapbox')
def mapbox():
    unbabelites = UnbabelitesHandler.get_all()

    return render_template('mapbox.html', mapbox_token=os.environ.get('MAPBOX_API_KEY'))
