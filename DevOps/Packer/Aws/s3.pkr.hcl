variable "access_key" {
  default = "YOUR_ACCESS_KEY"
}

variable "secret_key" {
  default = "YOUR_SECRET_KEY"
}

variable "region" {
  default = "us-west-2"
}

variable "source_ami" {
  default = "ami-0ff8a91507f77f867"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ssh_username" {
  default = "ubuntu"
}

variable "image_name" {
  default = "my-custom-image"
}

variable "install_script" {
  default = "install-software.sh"
}

resource "aws_instance" "example" {
  ami           = var.source_ami
  instance_type = var.instance_type

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

  connection {
    type        = "ssh"
    user        = var.ssh_username
    private_key = "${file("~/.ssh/id_rsa")}"
  }

  tags = {
    Name = var.image_name
  }
}

resource "aws_image" "example" {
  name          = var.image_name
  source_instance_id = aws_instance.example.id
}
