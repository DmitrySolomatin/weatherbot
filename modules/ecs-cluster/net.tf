# net.tf

# Availability Zones in the working region
data "aws_availability_zones" "available" {
}

resource "aws_vpc" "main" {
  cidr_block = "192.168.0.0/16"
  tags = {
    Name = "${var.app_name}-${var.environment}-VPC"
  }
}

# Create counter_for_az in private subnets
resource "aws_subnet" "private_subnet" {
  count             = var.counter_for_az
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id            = aws_vpc.main.id
  tags = {
    Name = "${var.app_name}-${var.environment}-private_subnet"
  }
}

# Create counter_for_az public subnets
resource "aws_subnet" "public_subnet" {
  count                   = var.counter_for_az
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, var.counter_for_az + count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.app_name}-${var.environment}-public_subnet"
  }
}

# Internet Gateway in public_subnet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.app_name}-${var.environment}-igw"
  }
}

# Route the public_subnet traffic with the IGW
resource "aws_route" "internet_access" {
  route_table_id         = aws_vpc.main.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Create a NAT gateway with an Elastic IP for each private subnet to get internet connectivity
resource "aws_eip" "igw" {
  count      = var.counter_for_az
  vpc        = true
  depends_on = [aws_internet_gateway.igw]
  tags = {
    Name = "${var.app_name}-${var.environment}-EIP"
  }
}

resource "aws_nat_gateway" "ngw" {
  count         = var.counter_for_az
  subnet_id     = element(aws_subnet.public_subnet.*.id, count.index)
  allocation_id = element(aws_eip.igw.*.id, count.index)
  tags = {
    Name = "${var.app_name}-${var.environment}-NGW"
  }
}

# Create a new route table for the private subnets, make it route non-local traffic through the NAT gateway to the internet
resource "aws_route_table" "private_rt" {
  count  = var.counter_for_az
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = element(aws_nat_gateway.ngw.*.id, count.index)
  }
  tags = {
    Name = "${var.app_name}-${var.environment}-RT"
  }
}

# Explicitly associate the newly created route tables to the private subnets (so they don't default to the main route table)
resource "aws_route_table_association" "private_subnet" {
  count          = var.counter_for_az
  subnet_id      = element(aws_subnet.private_subnet.*.id, count.index)
  route_table_id = element(aws_route_table.private_rt.*.id, count.index)
}

