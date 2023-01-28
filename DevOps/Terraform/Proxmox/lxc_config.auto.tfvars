lxc_linux = {

  /* List of LXC that will be provisioner by Terraform. If you want to create multiple just add a new LXC on the list by copying 
  the existing one and editing the configuration.*/

  // Configuration

  lxc1 = {
    target_node  = "yournode",
    name         = "name",
    memory       = "1024",
    cores        = "2",
    storage      = "local",
    disk_size    = "2G"
    ip           = "10.0.60.10",
    gw           = "10.0.60.1",
    ostemplate   = "local:vztmpl/OS_IMAGE",
    cmode        = "console",
    swap         = "0",
    nesting      = true,
    unprivileged = true,
    start        = true,
    env_config = [
      
    ]
  }

}


