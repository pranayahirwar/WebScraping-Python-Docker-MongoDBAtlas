# Terraform for IaC

I have used terraform to provision an `Standard_B1s` VM and then gradually increased the size of VM using GUI to test workload with more nodes.

Variables.tf
```HCL
variable "displayed_resource_theme" {
  default = "internship-assignment-vm"
}

variable "server_username" {
  default = "iavm"
}

variable "server_size" {
  default = "Standard_B1s"
}
```

Output.tf
```HCL
output "azure_vm_one_ip" {
  value = resource.azurerm_linux_virtual_machine.assignment-vm-one.public_ip_addresses
}

output "server_username" {
  value = var.server_username
}
```

Main.tf

```HCL

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}


resource "azurerm_resource_group" "assignment-rg" {
  name     = "${var.displayed_resource_theme}-resource-group"
  location = "centralindia"
}

resource "azurerm_virtual_network" "assignment-vnet" {
  name                = "${var.displayed_resource_theme}-virtual-net"
  location            = azurerm_resource_group.assignment-rg.location
  resource_group_name = azurerm_resource_group.assignment-rg.name
  address_space       = ["192.168.20.0/24"]
}

resource "azurerm_subnet" "assignment-sub1" {
  name                 = "${var.displayed_resource_theme}-subnet"
  resource_group_name  = azurerm_resource_group.assignment-rg.name
  virtual_network_name = azurerm_virtual_network.assignment-vnet.name
  #This subnet will containe 32 addresses among which Azure reserved 5 address for itself.
  address_prefixes = ["192.168.20.0/27"]
}

resource "azurerm_network_interface" "assignment-nic" {
  name                = "${var.displayed_resource_theme}-nic"
  location            = azurerm_resource_group.assignment-rg.location
  resource_group_name = azurerm_resource_group.assignment-rg.name

  ip_configuration {
    name                          = "${var.displayed_resource_theme}-ipconfig"
    subnet_id                     = azurerm_subnet.assignment-sub1.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.assignment-pubip.id
  }
}

resource "azurerm_public_ip" "assignment-pubip" {
  name                = "${var.displayed_resource_theme}-public-ip"
  location            = azurerm_resource_group.assignment-rg.location
  resource_group_name = azurerm_resource_group.assignment-rg.name
  allocation_method   = "Dynamic"
}


#//Security Group and Association

resource "azurerm_network_security_group" "assignment-nsg" {
  name                = "${var.displayed_resource_theme}-project-nsg"
  location            = "Central India"
  resource_group_name = resource.azurerm_resource_group.assignment-rg.name
}

resource "azurerm_network_security_rule" "allow_ssh" {
  name                        = "allow_ssh"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = resource.azurerm_resource_group.assignment-rg.name
  network_security_group_name = azurerm_network_security_group.assignment-nsg.name
}

resource "azurerm_network_security_rule" "selenium-grid-hub" {
  name                        = "selenium-grid-hub"
  priority                    = 201
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "4442-4444"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = resource.azurerm_resource_group.assignment-rg.name
  network_security_group_name = azurerm_network_security_group.assignment-nsg.name
}


resource "azurerm_network_interface_security_group_association" "assignment-nsg-a"{
  network_interface_id = azurerm_network_interface.assignment-nic.id
  network_security_group_id = azurerm_network_security_group.assignment-nsg.id
}

resource "azurerm_linux_virtual_machine" "assignment-vm-one" {
  name                            = "${var.displayed_resource_theme}-vm-one"
  location                        = azurerm_resource_group.assignment-rg.location
  resource_group_name             = azurerm_resource_group.assignment-rg.name
  size                            = var.server_size
  admin_username                  = var.server_username
  disable_password_authentication = true
  network_interface_ids           = [azurerm_network_interface.assignment-nic.id]


  admin_ssh_key {
    username   = var.server_username
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = 64

  }


  source_image_reference {
    publisher = "canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts-gen2"
    version   = "latest"
  }
  

  tags = {
    environment = "dev"
  }

}
```