variable "proxmox" {
  type = map(any)
  default = {
    url = "https://PROXMOX-URL:8006/api2/json"
    id  = "root@pam!YOURID"
    key = "YOUR-TOKEN"
  }
    sensitive = true
}

variable "password" {
  description = "initial ssh root password"
  type        = string
  default     = "root"
  sensitive   = true
}


variable "user" {
  description = "initial ssh root user"
  type        = string
  default     = "root"
  sensitive   = true
}


variable "ssh_keys" {
  description = "initial ssh keys"
  type        = map(any)
  default = {
    public  = "~/.ssh/YOURKEY.pub"
    private = "~/.ssh/YOURKEY"
  }
  sensitive = true
}

variable "lxc_linux" {
  description = "lxc config variables"
  type        = map(any)
}

variable "vm_linux" {
  description = "VM config variables"
  type        = map(any)
}

variable "vm_template" {
  description = "VM Template"
  type        = map(any)
  default = {
    TEMPLATE1 = "YOUR PAKCER TEMPLATE"
  }
}
