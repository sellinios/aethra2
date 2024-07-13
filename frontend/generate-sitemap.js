const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { SitemapStream, streamToPromise } = require('sitemap');
require('dotenv').config(); // Load environment variables from .env file

// Get hostname from environment variables
const hostname = process.env.REACT_APP_HOSTNAME || 'http://kairos.gr';
const langCode = 'en'; // Define the language code you want to use
const apiUrl = `${hostname}/api/${langCode}/places-with-urls/`;

if (process.env.NODE_ENV === 'development') {
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
}

// Function to fetch weather places data
async function fetchWeatherPlaces(page = 1, pageSize = 100) {
  try {
    const response = await axios.get(apiUrl, {
      params: { page, page_size: pageSize }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching weather places:', error);
    return { results: [], next: null };
  }
}

async function generateSitemap() {
  const links = [
    { url: '/', changefreq: 'daily', priority: 1.0 },
    { url: '/about', changefreq: 'monthly', priority: 0.8 },
    { url: '/contact', changefreq: 'monthly', priority: 0.8 },
    { url: '/geography/greece/municipalities', changefreq: 'monthly', priority: 0.8 },
  ];

  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const weatherPlacesData = await fetchWeatherPlaces(page);
    if (!weatherPlacesData.results.length) {
      hasMore = false;
      break;
    }

    weatherPlacesData.results.forEach(place => {
      if (place && place.url) {
        links.push({ url: place.url, changefreq: 'daily', priority: 0.9 });
      }
    });

    page++;
    hasMore = !!weatherPlacesData.next;
  }

  const sitemap = new SitemapStream({ hostname });
  links.forEach(link => sitemap.write(link));
  sitemap.end();

  streamToPromise(sitemap).then(sm => {
    const sitemapPath = path.resolve(__dirname, 'public', 'sitemap.xml');
    fs.writeFileSync(sitemapPath, sm.toString());
    console.log(`Sitemap written successfully to ${sitemapPath}`);
  }).catch(console.error);
}

generateSitemap();