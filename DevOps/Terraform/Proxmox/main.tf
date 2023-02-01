# LXC

resource "proxmox_lxc" "lxc_linux" {

  for_each = var.lxc_linux

  target_node     = each.value.target_node
  hostname        = each.value.name
  cmode           = each.value.cmode
  ostemplate      = each.value.ostemplate
  memory          = each.value.memory
  swap            = each.value.swap
  cores           = each.value.cores
  unprivileged    = each.value.unprivileged
  start           = each.value.start
  password        = var.password
  onboot          = each.value.onboot
  ssh_public_keys = file(var.ssh_keys["public"])


  features {
    nesting = each.value.nesting
  }

  rootfs {
    storage = each.value.storage
    size    = each.value.disk_size
  }

  network {
    name   = "eth0"
    bridge = "vmbr0"
    ip     = "${each.value.ip}/24"
    gw     = each.value.gw
  }

  // Post-configuration settings

  connection {
    type = "ssh"
    //user        = var.user
    password    = var.password
    private_key = file(var.ssh_keys["private"])
    host        = each.value.ip
    timeout     = "180m"
  }

  provisioner "remote-exec" {
    inline = each.value.env_config
  }

}

#imported proxmox lxc : command terraform import proxmox_lxc.VM_Name lab/lxc/ID

# VMs

resource "proxmox_vm_qemu" "vm_linux" {

  for_each = var.vm_linux

  name        = each.value.name
  desc        = each.value.desc
  target_node = each.value.target_node
  full_clone  = true
  memory      = each.value.memory
  sockets     = "1"
  cores       = "4"
  cpu         = "host"
  scsihw      = "virtio-scsi-pci"
  clone       = var.vm_template["Clean"]
  agent       = 1
  onboot      = true
  oncreate    = true



  disk {
    size    = each.value.disk_size
    type    = "virtio"
    storage = "local"
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  # Cloud-init section
  os_type                = "cloud-init"
  define_connection_info = true
  ipconfig0              = "ip=dhcp"
  ciuser                 = var.user
  cipassword             = var.password
  sshkeys                = file(var.ssh_keys["public"])


  # Post creation actions
  connection {
    type = "ssh"
    //user        = var.user
    password    = var.password
    private_key = file(var.ssh_keys["private"])
    host        = self.ssh_host
    timeout     = "180m"
  }

  provisioner "remote-exec" {
    inline = each.value.env_config
  }

}

#imported proxmox vm : command terraform import proxmox_vm_qemu.VM_Name lab/vm/ID