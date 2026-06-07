terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_container" "postgres_db" {
  name  = "db-ventas"
  image = "postgres:15"
  
  ports {
    internal = 5432
    external = 5432
  }

  env = [
    "POSTGRES_USER=admin",
    "POSTGRES_PASSWORD=secret123",
    "POSTGRES_DB=ventas_db"
  ]
}