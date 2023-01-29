variable "project_id" {
  default = "my-gcp-project"
}

variable "zone" {
  default = "us-central1-a"
}

variable "ssh_username" {
  default = "ubuntu"
}

variable "source_image_family" {
  default = "ubuntu-2004-lts"
}

variable "image_name" {
  default = "my-custom-image"
}

variable "image_description" {
  default = "A custom image with Ubuntu 20.04 and additional software installed"
}

variable "install_script" {
  default = "install-software.sh"
}

resource "googlecompute_image" "image" {
  name        = var.image_name
  project     = var.project_id
  family      = var.source_image_family
  description = var.image_description
}

resource "googlecompute_instance" "instance" {
  name         = "packer-temp"
  machine_type = "f1-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = googlecompute_image.image.self_link
    }
  }

  metadata = {
    packer-build-name = "image"
    packer-builder-type = "googlecompute"
  }

  service_account {
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  connection {
    type     = "ssh"
    user     = var.ssh_username
    private_key = file("~/.ssh/id_rsa")
  }

  provisioner "file" {
    source      = var.install_script
    destination = "/tmp/install-software.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/install-software.sh",
      "sudo /tmp/install-software.sh"
    ]
  }
}
