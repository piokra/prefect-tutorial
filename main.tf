terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "1.23.0"
    }
  }


  backend "remote" {
    organization = "piokra"

    workspaces {
      name = "prefect-tutorial"
    }
  }

}

provider "hcloud" {
  token = var.hcloud_token
}

data "hcloud_network" "visibility_network" {
  name = "network-1"
}

resource "hcloud_ssh_key" "agent_admin_ssh_key" {
  name       = "agent_admin_ssh_key-1"
  public_key = var.ssh_public_key
}


resource "hcloud_server" "agent" {
  count       = var.node_count
  name        = "node-${count.index + 1}"
  server_type = var.node_type
  image       = var.node_image
  ssh_keys = [
  hcloud_ssh_key.agent_admin_ssh_key.id]

  connection {
    host        = self.ipv4_address
    type        = "ssh"
    private_key = var.ssh_private_key
  }

  provisioner "file" {
    source      = "terraform/files/Dockerfile"
    destination = "/root/Dockerfile"
  }

  provisioner "file" {
    source      = "terraform/scripts/bootstrap.sh"
    destination = "/root/bootstrap.sh"
  }

  provisioner "file" {
    source      = "requirements.txt"
    destination = "/root/requirements.txt"
  }

  provisioner "file" {
    source      = "spryframework"
    destination = "/root"
  }

  provisioner "file" {
    source      = path.root
    destination = "/root"

  }

  provisioner "remote-exec" {
    inline = [
    "VAULT_URL=${var.vault_url} VAULT_TOKEN=${var.vault_token} DOCKER_VERSION=${var.docker_version} TOKEN=${var.prefect_runner_token} bash /root/bootstrap.sh"]
  }
}

resource "hcloud_server_network" "visibility_server_network" {
  count      = var.node_count
  server_id  = hcloud_server.agent.*.id[count.index]
  network_id = data.hcloud_network.visibility_network.id
}
