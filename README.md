# ChartSync

Utility to sync charts located in local filesystem with remote or local [ChartMuseum](https://chartmuseum.com/docs/).

Let's say you have a cloud native project with microservices. In an ideal world, you'd have a CI/CD pipeline which
produces up-to-date helm charts in a repository.

This tool tries to help the less fortunate, and provides a (semi) automated way to publish/export charts located on your
local filesystem.