This is a simple tool to load the firmware on a "FIBER/CO2-V" board and use lightburn on linux.

Those board enumerate as as 9588:9880 when they are powered-up and 9588:9899 after the fpga image is loaded. This tool will extract the firmware from the Windows `Lmcv2u.sys` driver and load it on an un-initialized board.

To run the tool, make sure you have pyUsb installed (`pip install pyUsb`) and that you have your `Lmcv2u.sys` file in your working directory.