# Google search

## Download Files

Uses the `requests` lib to search for files on google and download them inside a local directory.

### Usage

`search(query='pdf', download_path=filepath)`

**Params:**
- query: the search terms, 
- download_path: directory path to save the files, 
- filetype: the type of file to search for (defaults to `pdf`), 
- language: which language the files should be (defaults to `pt-BR`), 
- as_qdr: google search parameter, not yet defined (defaults to 'all')
- count: how many files shall be downloaded

## TO DO:
- [ ] Fix download when there is no content-length
- [ ] Add timeout when saving the file