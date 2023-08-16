git clone https://github.com/opensearch-project/project-website.git --depth=1
git clone https://github.com/opensearch-project/documentation-website.git --depth=1

mkdir data

brew install ruby
gem install bundler jekyll

cd project-website
bundle install
bundle exec jekyll build
mv _site/search-index.json ../data/website-index.json
cd ..

cd documentation-website
bundle install
bundle exec jekyll build
mv _site/search-index.json ../data/documentation-index.json

cd ..
rm -rf project-website
rm -rf documentation-website
