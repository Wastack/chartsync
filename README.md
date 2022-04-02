# ChartSync

Utility to sync charts located in local filesystem with remote or local [ChartMuseum](https://chartmuseum.com/docs/).

Let's say you have a cloud native project with microservices. In an ideal world, you'd have a CI/CD pipeline which
produces up-to-date helm charts in a repository.

This tool tries to help the less fortunate, and provides a (semi) automated way to publish/export charts located on your
local filesystem.

## requirements

```bash
pip install -r requirements.txt
```

## Usage

You can use `config.yaml` to provide a list of charts on the filesystem. Example:

```yaml
logLevel: 20
chartMuseum:
  url: "http://localhost:8080"
  overwriteExisting: true

# List of charts to export
charts:
  - path: "/path/to/a/chart"
  - path: "/path/to/another/chart"
```

Make sure you have ChartMuseum running, and you are ready to export:

```bash
python main.py
```