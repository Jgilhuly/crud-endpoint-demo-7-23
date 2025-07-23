# Product CRUD API with Advanced Search

A FastAPI-based product management system with comprehensive search functionality.

## Features

### Core Features
- ✅ Create, Read, Update, Delete (CRUD) operations for products
- ✅ Web interface with Bootstrap styling
- ✅ In-memory database with sample data
- ✅ Form-based product management

### 🔍 New Search Features

#### 1. Advanced Search Interface
- **Dedicated search page** at `/search` with comprehensive filters
- **Quick search bar** on the main products page
- **Real-time filtering** without page reloads
- **Grid and list view** toggle for search results

#### 2. Search Criteria
- **Text Search**: Search by product name and description
- **Category Filter**: Filter by product categories
- **Price Range**: Set minimum and maximum price filters
- **Stock Status**: Filter by in-stock or out-of-stock items
- **Tags**: Search by product tags (comma-separated)

#### 3. API Endpoints

##### Search Products
```
GET /api/search
```
**Parameters:**
- `query` (optional): Text search term
- `category` (optional): Product category
- `min_price` (optional): Minimum price
- `max_price` (optional): Maximum price
- `in_stock` (optional): Stock status (true/false)
- `tags` (optional): Comma-separated tags

**Example:**
```bash
curl "http://localhost:8000/api/search?query=wireless&category=Electronics&min_price=100"
```

##### Get Categories
```
GET /api/categories
```
Returns all available product categories.

##### Get Tags
```
GET /api/tags
```
Returns all available product tags.

#### 4. Web Interface

##### Main Search Page
- Access via `/search` or click "Search" in navigation
- Comprehensive filter form with all search criteria
- Live results display with count
- Quick tag filters for easy selection

##### Quick Search
- Available on main products page (`/`)
- Real-time filtering as you type
- Searches across name, description, category, and tags

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python main.py
```

The server will start at `http://localhost:8000`

## Usage Examples

### Web Interface
1. **Main Products Page**: `http://localhost:8000/`
   - View all products
   - Use quick search bar for instant filtering
   - Access advanced search

2. **Advanced Search**: `http://localhost:8000/search`
   - Use multiple filters simultaneously
   - Switch between grid and list views
   - Click tag filters for quick searches

### API Usage

#### Search for wireless products
```bash
curl "http://localhost:8000/api/search?query=wireless"
```

#### Filter by category and price range
```bash
curl "http://localhost:8000/api/search?category=Electronics&min_price=50&max_price=200"
```

#### Search by tags
```bash
curl "http://localhost:8000/api/search?tags=audio,portable"
```

#### Complex search with multiple criteria
```bash
curl "http://localhost:8000/api/search?query=speaker&category=Electronics&min_price=50&in_stock=true&tags=audio"
```

## Project Structure

```
/workspace/
├── main.py              # FastAPI application with search endpoints
├── models.py            # Pydantic models for products
├── database.py          # In-memory database with search methods
├── requirements.txt     # Python dependencies
├── templates/
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Main products page with quick search
│   ├── search.html      # Advanced search interface
│   ├── new.html         # Add product form
│   └── edit.html        # Edit product form
└── static/
    ├── css/
    │   └── style.css    # Custom styling with search enhancements
    └── js/
        └── app.js       # JavaScript for search functionality
```

## Search Implementation Details

### Backend Search Logic
The search functionality is implemented in `database.py` with the `search_products()` method:

- **Text matching**: Case-insensitive search across product names and descriptions
- **Category filtering**: Exact match (case-insensitive)
- **Price range**: Numerical comparison with optional min/max bounds
- **Stock status**: Boolean filtering
- **Tag matching**: Supports multiple tags with "any match" logic

### Frontend Features
- **Real-time filtering**: JavaScript-based instant search on main page
- **Form persistence**: Search parameters maintained across page loads
- **Responsive design**: Mobile-friendly search interface
- **Visual feedback**: Results counter and hover effects
- **Accessibility**: Proper labels and keyboard navigation

## Sample Data

The application includes 6 sample products across different categories:
- Electronics (3 items): Wireless Headphones, Bluetooth Speaker, Smart Watch
- Appliances (1 item): Coffee Maker
- Accessories (1 item): Laptop Stand  
- Furniture (1 item): Office Chair

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

## Future Enhancements

Potential improvements for the search functionality:
- Elasticsearch integration for full-text search
- Search history and saved searches
- Advanced filtering (date ranges, multi-select categories)
- Search suggestions and autocomplete
- Sort options (price, name, date, relevance)
- Pagination for large result sets 