vm_linux = {

  /* List of VMs that will be provisioner by Terraform. If you want to create multiple just add a new VMs on the list by copying 
  the existing one and editing the configuration.*/

  // Configuration
  VM1 = {

    target_node = "YOUR-NODE",
    name        = "VM-NAME",
    desc        = "Description",
    vcpu        = "4",
    memory      = "6144",
    disk_size   = "50G",
    ip          = "VM-IP",
    gw          = "NET-Gateway",

    env_config = [
      
    ]
  }
}
