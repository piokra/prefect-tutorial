terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "1.23.0"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_ssh_key" "agent_admin_ssh_key" {
  name       = "agent_admin_ssh_key-1"
  public_key = file(var.ssh_public_key)
}

resource "hcloud_server" "agent" {
  count       = var.node_count
  name        = "node-${count.index + 1}"
  server_type = var.node_type
  image       = var.node_image
  ssh_keys    = [hcloud_ssh_key.agent_admin_ssh_key.id]

  connection {
    host        = self.ipv4_address
    type        = "ssh"
    private_key = file(var.ssh_private_key)
  }

  provisioner "file" {
    source      = "files/Dockerfile"
    destination = "/root/Dockerfile"
  }

  provisioner "file" {
    source      = "scripts/bootstrap.sh"
    destination = "/root/bootstrap.sh"
  }

  provisioner "remote-exec" {
    inline = ["DOCKER_VERSION=${var.docker_version} TOKEN=${var.prefect_runner_token} bash /root/bootstrap.sh"]
  }
}

