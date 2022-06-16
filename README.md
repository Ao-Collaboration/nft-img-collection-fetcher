# NFT Image Collection Fetcher

Download all NFTs from a collection.

## Usage

1. Find the collection contract on Etherscan.
2. Go to Contract > Read Contract.
3. Find the `tokenURI` method, input a token id and `Query`.
4. Replace the token id with `{}`.
5. Find the first and last token id.
6. Run the script with `py fetch_images.py`
7. Input the data obtained above when prompted.
