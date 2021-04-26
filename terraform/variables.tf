variable "hcloud_token" {
}

variable "prefect_runner_token" {
}

variable "node_image" {
  description = "Predefined Image that will be used to spin up the machines (Currently supported: ubuntu-20.04, ubuntu-18.04)"
  default     = "ubuntu-20.04"
}

variable "node_type" {
  description = "For more types have a look at https://www.hetzner.de/cloud"
  default     = "cx11"
}

variable "node_count" {
  default = 1
}

variable "docker_version" {
  default = "20.10"
}

variable "ssh_private_key" {
  description = "Private Key to access the machines"
}

variable "ssh_public_key" {
  description = "Public Key to authorized the access for the machines"
}
