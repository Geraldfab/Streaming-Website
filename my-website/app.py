from flask import Flask, render_template, request, jsonify, url_for
import requests

app = Flask(__name__, static_folder='static')

# TMDB API Configuration
API_KEY = 'babd261dc0b8f207fe4442292955e654'
BASE_URL = 'https://api.themoviedb.org/3'
IMG_URL = 'https://image.tmdb.org/t/p/original'

def get_image_url(path, size='original'):
    """Generate TMDB image URL"""
    if path:
        return f"{IMG_URL.replace('/original', f'/{size}')}{path}"
    return None

@app.route('/')
def home():
    """Home page with trending content"""
    return render_template('home.html', api_key=API_KEY, img_url=IMG_URL)

@app.route('/movies')
def movies():
    """Movies page with various categories"""
    return render_template('movies.html', api_key=API_KEY, img_url=IMG_URL)

@app.route('/tvshows')
def tvshows():
    """TV Shows page with various categories"""
    return render_template('tvshows.html', api_key=API_KEY, img_url=IMG_URL)

@app.route('/anime')
def anime():
    """Anime page with categorization"""
    return render_template('anime.html', api_key=API_KEY, img_url=IMG_URL)

@app.route('/categories')
def categories():
    """Categories page with all content types"""
    return render_template('categories.html', api_key=API_KEY, img_url=IMG_URL)

@app.route('/search')
def search():
    """Search results page"""
    query = request.args.get('q', '')
    return render_template('search.html', api_key=API_KEY, img_url=IMG_URL, query=query)

# API Routes for fetching data
@app.route('/api/trending/<type>')
def api_trending(type):
    """Get trending content"""
    period = request.args.get('period', 'week')
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/trending/{type}/{period}?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/movies/popular')
def api_movies_popular():
    """Get popular movies"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/movies/top_rated')
def api_movies_top_rated():
    """Get top rated movies"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/movies/now_playing')
def api_movies_now_playing():
    """Get now playing movies"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/movie/now_playing?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/movies/upcoming')
def api_movies_upcoming():
    """Get upcoming movies"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/movie/upcoming?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/tv/popular')
def api_tv_popular():
    """Get popular TV shows"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/tv/popular?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/tv/top_rated')
def api_tv_top_rated():
    """Get top rated TV shows"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/tv/top_rated?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/tv/on_the_air')
def api_tv_on_the_air():
    """Get TV shows on the air"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/tv/on_the_air?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/tv/<int:tvmdb_id>/season')
def api_tv_seasons(tvmdb_id):
    """Get TV show seasons"""
    url = f"{BASE_URL}/tv/{tvmdb_id}?api_key={API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/tv/<int:tvmdb_id>/season/<int:season_number>')
def api_tv_season_details(tvmdb_id, season_number):
    """Get season details with episodes"""
    url = f"{BASE_URL}/tv/{tvmdb_id}/season/{season_number}?api_key={API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/discover/anime')
def api_discover_anime():
    """Get anime content"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/discover/tv?api_key={API_KEY}&page={page}&with_original_language=ja&with_genres=16"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/discover/anime/popular')
def api_anime_popular():
    """Get popular anime"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/discover/tv?api_key={API_KEY}&page={page}&with_original_language=ja&with_genres=16&sort_by=popularity.desc"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/discover/anime/top_rated')
def api_anime_top_rated():
    """Get top rated anime"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/discover/tv?api_key={API_KEY}&page={page}&with_original_language=ja&with_genres=16&sort_by=vote_average.desc&vote_count.gte=100"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/discover/anime/airing')
def api_anime_airing():
    """Get currently airing anime"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/discover/tv?api_key={API_KEY}&page={page}&with_original_language=ja&with_genres=16&airing_status=1"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/categories')
def api_categories():
    """Get all available categories"""
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/genre/<type>/<genre_id>')
def api_genre_content(type, genre_id):
    """Get content by genre"""
    page = request.args.get('page', '1')
    sort_by = request.args.get('sort_by', 'popularity.desc')
    url = f"{BASE_URL}/discover/{type}?api_key={API_KEY}&page={page}&with_genres={genre_id}&sort_by={sort_by}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/search')
def api_search():
    """Search for movies, TV shows, and anime"""
    query = request.args.get('query', '')
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/search/multi?api_key={API_KEY}&query={query}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/details/<type>/<id>')
def api_details(type, id):
    """Get detailed information about a movie or TV show"""
    url = f"{BASE_URL}/{type}/{id}?api_key={API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/api/similar/<type>/<id>')
def api_similar(type, id):
    """Get similar content"""
    page = request.args.get('page', '1')
    url = f"{BASE_URL}/{type}/{id}/similar?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
