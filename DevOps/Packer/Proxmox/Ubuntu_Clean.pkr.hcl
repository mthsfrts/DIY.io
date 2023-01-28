# Ubuntu Server Focal
# ---
# Variables
variable "proxmox_api_url" {
  type = string
}

variable "proxmox_api_token_id" {
  type = string
}

variable "proxmox_api_token_secret" {
  type      = string
  sensitive = true
}

variable "username" {
  description = "initial ssh root user"
  type        = string
  sensitive   = true
}

variable "password" {
  description = "initial ssh root password"
  type        = string
  sensitive   = true
}


# Resource Definiation for the VM Template
source "proxmox-iso" "ubuntu-server-focal" {

  # Proxmox Connection Settings
  proxmox_url = "${var.proxmox_api_url}"
  username    = "${var.proxmox_api_token_id}"
  token       = "${var.proxmox_api_token_secret}"

  # (Optional) Skip TLS Verification
  insecure_skip_tls_verify = true

  # VM General Settings
  node                 = "lab"
  vm_id                = "201"
  vm_name              = "ubuntu-clean"
  template_description = "Ubuntu 20.04, generated on {{ isotime \"2006-01-02T15:04:05Z\" }}"

  # VM OS Settings
  # (Option 1) Local ISO File

  iso_file = "local:iso/ubuntu-20.04-live-server-amd64.iso"

  # (Option 2) Download ISO

  # iso_url      = "https://old-releases.ubuntu.com/releases/focal/ubuntu-20.04-live-server-amd64.iso"
  # iso_checksum = "caf3fd69c77c439f162e2ba6040e9c320c4ff0d69aad1340a514319a9264df9f"

  iso_storage_pool = "local"
  unmount_iso      = true

  # VM System Settings
  qemu_agent = true

  # VM Hard Disk Settings
  scsi_controller = "virtio-scsi-pci"

  disks {
    disk_size         = "50G"
    format            = "raw"
    storage_pool      = "local"
    storage_pool_type = "lvm"
    type              = "virtio"
  }

  # VM CPU Settings
  cores = "4"

  # VM Memory Settings
  memory = "6144"

  # VM Network Settings
  network_adapters {
    model    = "virtio"
    bridge   = "vmbr0"
    firewall = true
  }

  # VM Cloud-Init Settings
  cloud_init              = true
  cloud_init_storage_pool = "local"

  # PACKER Boot Commands
  boot_command = [

    "<esc><wait><esc><wait>",
    "<f6><wait><esc><wait>",
    "<bs><bs><bs><bs><bs><bs>",
    " autoinstall ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/ ",
    "--- <enter>"
  ]

  boot      = "c"
  boot_wait = "5s"

  # PACKER Autoinstall Settings

  # HTTP Settings

  #Folder Path Settings
  http_directory = "http"

  # (Optional) Bind IP Address and Port
  http_bind_address = "10.0.60.10"
  http_port_min     = 8802
  http_port_max     = 8802

  # SSH Settings
  ssh_username           = "${var.username}"
  ssh_password           = "${var.password}"
  ssh_handshake_attempts = "500"
  ssh_pty                = true
  communicator           = "ssh"

  # (Option 2) Add your Private SSH KEY file here
  ssh_private_key_file = "~/.ssh/your_SSH_private_"

  # Raise the timeout, when installation takes longer
  ssh_timeout = "180m"

}

# Build Definition to create the VM Template
build {

  name    = "ubuntu-server-focal"
  sources = ["source.proxmox-iso.ubuntu-server-focal"]

  # Provisioning the VM Template for Cloud-Init Integration in Proxmox #1
  provisioner "shell" {
    inline = [
      "while [ ! -f /var/lib/cloud/instance/boot-finished ]; do echo 'Waiting for cloud-init...'; sleep 1; done",
      "sudo rm /etc/ssh/ssh_host_*",
      "sudo truncate -s 0 /etc/machine-id",
      "sudo apt -y autoremove --purge",
      "sudo apt -y clean",
      "sudo apt -y autoclean",
      "sudo cloud-init clean",
      "sudo rm -f /etc/cloud/cloud.cfg.d/subiquity-disable-cloudinit-networking.cfg",
      "sudo sync"
    ]
  }

  # Provisioning the VM Template for Cloud-Init Integration in Proxmox #2
  provisioner "file" {
    source      = "file/99-pve.cfg"
    destination = "/tmp/99-pve.cfg"
  }

  # Provisioning the VM Template for Cloud-Init Integration in Proxmox #3
  provisioner "shell" {
    inline = ["sudo cp /tmp/99-pve.cfg /etc/cloud/cloud.cfg.d/99-pve.cfg"]
  }
}