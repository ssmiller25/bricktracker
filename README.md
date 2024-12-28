# BrickTracker

A web application for organizing and tracking LEGO sets, parts, and minifigures. Uses the Rebrickable API to fetch LEGO data and allows users to track missing pieces and collection status.

> **Screenshots at the end of the readme!**

<a href="https://www.buymeacoffee.com/frederikb" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Features

- Track multiple LEGO sets with their parts and minifigures
- Mark sets as checked/collected
- Track missing pieces
- View parts inventory across sets
- View minifigures across sets
- Automatic updates for LEGO data (themes, colors, sets)
- Wishlist to keep track of what to buy

## Prerequisites

- Docker
- Docker Compose
- Rebrickable API key (from [Rebrickable](https://rebrickable.com/api/))

## Setup

1. Clone the repository:
```bash
git clone https://gitea.baerentsen.space/FrederikBaerentsen/BrickTracker.git
cd BrickTracker
mkdir static/{sets,instructions,parts,minifigs}
```

2. Create a `.env` file with your configuration:
```
REBRICKABLE_API_KEY=your_api_key_here
DOMAIN_NAME=https://your.domain.com
```

If using locally, set `DOMAIN_NAME` to `http://localhost:3333`.

```
LINKS=True
```
Can be added to the `.env` file in order for set numbers to be links to Rebrickable on the front page. 

3. Deploy with Docker Compose:
```bash
docker compose up -d
```

4. Access the web interface at `http://localhost:3333`

5. The database is created, csv files are downloaded and you will be redirected to the `/create` page for inputting a set number.

## Setup using pre-build Docker image

1. Setup folders and files:
```bash
mkdir BrickTracker
cd BrickTracker
mkdir -p static/{sets,instructions,parts,minifigs}
touch app.db
```

2. Create Docker Compose file:
```bash
services:
  bricktracker:
    container_name: BrickTracker
    restart: unless-stopped
    image: gitea.baerentsen.space/frederikbaerentsen/bricktracker:latest
    ports:
      - "3333:3333"
    volumes:
      - ./.env:/app/.env
      - ./static/parts:/app/static/parts
      - ./static/instructions:/app/static/instructions
      - ./static/sets:/app/static/sets
      - ./static/minifigs:/app/static/minifigs
      - ./app.db:/app/app.db
    environment:
      - REBRICKABLE_API_KEY=your_api_key_here
      - DOMAIN_NAME=https://your.domain.com
      - LINKS=True #optional, enables set numbers to be Rebrickable links on the front page.
```

If using locally, set `DOMAIN_NAME` to `http://localhost:3333`.

3. Deploy with Docker Compose:
```bash
docker compose up -d
```

4. Access the web interface at `http://localhost:3333`

5. The database is created, csv files are downloaded and you will be redirected to the `/create` page for inputting a set number.

6. csv files are downloaded inside the container. If you delete the container, go to `/config` and redownload them again. 

## Usage

### Adding Sets
1. Go to the Create page
2. Enter a LEGO set number (e.g., "42115")
3. Wait for the set to be downloaded and processed

### Managing Sets
- Mark sets as checked/collected using the checkboxes
- Track missing pieces by entering quantities in the parts table
    - Note, the checkbox for missing pieces is updated automatically, if the set has missing pieces. It cannot be manually checked off.
- View all missing pieces across sets in the Missing page
- View complete parts inventory in the Parts page
- View all minifigures in the Minifigures page

### Instructions

Instructions can be added to the `static/instructions` folder. Instructions **must** be named:

- SetNumber.pdf: `10312-1.pdf` or `7001-1.pdf`. Sets with multiple versions (eg. collectible minifigures use `-1`, `-2` etc) like `71039-1.pdf` and `71039-2.pdf`.
- SetNumber-pdf_number.pdf: `10294-1-1.pdf`, `10294-1-2.pdf` and `10294-1-3.pdf` for all three PDFs of the `10294-1` set.

Instructions are not automatically downloaded!

## Docker Configuration

The application uses two main configuration files:

### docker-compose.yml
```yaml
services:
  bricktracker:
    container_name: BrickTracker
    restart: unless-stopped
    build: .
    ports:
      - "3333:3333"
    volumes:
      - .:/app
    env_file:
      - .env
```

### Dockerfile
```dockerfile
FROM python:slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN bash lego.sh
CMD ["gunicorn","--bind","0.0.0.0:3333","app:app","--worker-class","eventlet"]
```

## Development

The application is built with:
- Flask (Python web framework)
- SQLite (Database)
- Socket.IO (Real-time updates)
- Rebrickable API (LEGO data)

Key files:
- `app.py`: Main application code
- `db.py`: Database operations
- `downloadRB.py`: Rebrickable data download utilities

## Notes

- The application stores images locally in the `static` directory
- Database is stored in `app.db` (SQLite)
- LEGO data is cached in CSV files from Rebrickable
- Images are downloaded from Rebrickable when entering a set and then stored locally.
- The code is AS-IS! I am not a professional programmer and this has been a hobby projects for a long time. Don't expect anything neat! 

## Screenshots

### Front page 
![](https://xbackbone.baerentsen.space/LaMU8/koLAhiWe94.png/raw)

Search your inventory and sort by theme, year, parts, id, name or sort by missing pieces. If you download instructions as PDF, add them to a specific folder and they show up [under each set](https://xbackbone.baerentsen.space/LaMU8/ZIyIQUdo31.png/raw)

### Inventory

![](https://xbackbone.baerentsen.space/LaMU8/MeXaYuVI44.png/raw)

Filter by color, quantity, name. Add if a piece is missing. Press images to [show them](https://xbackbone.baerentsen.space/LaMU8/FIFOQicE66.png/raw). Filter by only [missing pieces](https://xbackbone.baerentsen.space/LaMU8/LUQeTETA28.png). Minifigures and their parts are listed [at the end](https://xbackbone.baerentsen.space/LaMU8/nEPujImi75.png/raw).

### Missing pieces

![](https://xbackbone.baerentsen.space/LaMU8/YEPEKOsE50.png/raw)

List of all your missing pieces, with links to bricklink and rebrickable. 

### All parts

![](https://xbackbone.baerentsen.space/LaMU8/TApONAkA94.png/raw)
List of all parts in your inventory.

### Minifigures

![](https://xbackbone.baerentsen.space/LaMU8/RuWoduFU08.png/raw)

List of all minifigures in your inventory and quantity.

### Multiple sets

![](https://xbackbone.baerentsen.space/LaMU8/BUHAYOYe40.png/raw)

Each set is given a unique ID, such that you can have multiple copies of a set with different pieces missing in each copy. Sets can also easily be [deleted](https://xbackbone.baerentsen.space/LaMU8/xeroHupE22.png/raw) from the inventory. 

### Add set

![](https://xbackbone.baerentsen.space/LaMU8/lAlUcOhE38.png/raw)

Sets are added from rebrickable using your own API key. Set numbers are checked against sets.csv from rebrickable and can be updated from the [config page](https://xbackbone.baerentsen.space/LaMU8/lErImaCE12.png/raw). When a set is added, all images from rebrickable are downloaded and stored locally, so if multiple sets contains the same part/color, only one image is downloaded and stored. This also make no calls to rebrickable when just browsing and using the site. Only time rebrickable to used it when up adding a new set. 

### Wishlist

![](https://xbackbone.baerentsen.space/LaMU8/hACAbArO44.png/raw)

Sets are added from rebrickable and again checked against sets.csv. If you can't add a brand new set, consider updating your data from the [`/config` page](https://xbackbone.baerentsen.space/LaMU8/lErImaCE12.png/raw). Press the delete button to remove a set. Known Issue: If multiple sets of the same number is added, they will all be deleted.


