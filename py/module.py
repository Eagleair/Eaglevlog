#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
import re
import align

from importlib import reload
reload(align)

class Module:
    
    name = 'init_name'
    ports = []
    file_str = ''
    inst_str = 'init_inst'
    tb_str = ''

    def __init__(self):
        self.name = 'init_name'
        self.ports = []
        self.file_str = ''
        self.inst_str = 'init_inst'
        self.tb_str = ''

    def init_module(self,file_str):
        if isinstance(file_str,str):
            self.file_str = file_str
        else:
            raise ValueError('bad file_str')
        search_module = re.search('^\s*module\s*\w+\s*\((.|\n)+\);$',self.file_str,re.M)
        if search_module:
                pass
        clean_port = re.sub('(input|output|inout)(\s+reg|\s+wire)?(\s*\[.*\])?\s*','',search_module.group())
        if clean_port:
                pass
        port_list = re.findall('\w+',clean_port)
        if port_list:
                pass
        self.name = port_list[1]
        for port_name in port_list[2:]:
            self.ports.append({ 'name':port_name,'iodir':'input','datah':0,'datal':0,'datatype':'wire' })
        for ports_index in range(len(self.ports)):
            port_search_result = re.search('(input|output|inout)\s*(reg|wire)?(\s*\[(\d*):(\d*)\])?\s*.*'+self.ports[ports_index]['name']+'',file_str)
            if port_search_result.group(1):
                self.ports[ports_index].update({'iodir': port_search_result.group(1) })
            if port_search_result.group(2):
                self.ports[ports_index].update({'datatype': port_search_result.group(2) })
            if port_search_result.group(4):
                self.ports[ports_index].update({ 'datah': port_search_result.group(4) })
            if port_search_result.group(5):
                self.ports[ports_index].update({ 'datal': port_search_result.group(5) })
            port_search_result = re.search('^\s*(reg|wire)(\s*\[(\d*):(\d*)\])?\s*.*'+self.ports[ports_index]['name']+'',file_str,re.M)
            if port_search_result:
                if port_search_result.group(1):
                    self.ports[ports_index].update({ 'datatype': port_search_result.group(1) })
                if port_search_result.group(3):
                    self.ports[ports_index].update({ 'datah': port_search_result.group(3) })
                if port_search_result.group(4):
                    self.ports[ports_index].update({ 'datal': port_search_result.group(4) })
    
    def add_head(name,author='Zhiying Zheng'):
        import time
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        year = now_time[0:4]
        string = "// -----------------------------------------------------------------\n//                 Copyright (c) %s .\n//                       ALL RIGHTS RESERVED\n// -----------------------------------------------------------------\n// Filename      : %s.v\n// Author        : %s\n// Created On    : %s\n// Last Modified :\n// -----------------------------------------------------------------\n// Description:\n//\n// -----------------------------------------------------------------\n"%(year,name,author,now_time)
        return string

    def get_inst(self, f_str, ints = 1, tabs = 4):
        Module.init_module(self, f_str)
        self.port_str=''
        for port in self.ports[:-1]:
            self.port_str += ' .' + port['name'] + ' ( ' + port['name'] + ' ),' 
            self.port_str += '\n'
        self.port_str += ' .' + self.ports[-1]['name'] + ' ( ' + self.ports[-1]['name'] + ' )' 
        self.inst_str = ints*'\t' + self.name + ' ' + self.name + '_inst(' 
        self.inst_str += '\n'
        self.inst_str += align.align(self.port_str,tabs,ints+1)
        self.inst_str += '\n'
        self.inst_str += ints*'\t' + ');'
        self.inst_str += '\n'
        return self.inst_str

    def get_tb(self, f_str, ints = 1, tabs = 4):
        Module.init_module(self, f_str)
        self.init_reg = ''
        self.tb_str = Module.add_head(self.name)
        self.tb_str += '`timescale 1ns/1ps' 
        self.tb_str += '\n\n' 
        self.tb_str += 'module ' + self.name + '_tb;' 
        self.tb_str += '\n' 
        for port in self.ports:
            if port['iodir'] == 'input':
                self.tb_str += '\treg [' + str(port['datah']) + ':' + str(port['datal']) + '] ' + port['name'] + ';\n'
        self.tb_str += '\n' 
        for port in self.ports:
            if port['iodir'] == 'output':
                self.tb_str += '\twire [' + str(port['datah']) + ':' + str(port['datal']) + '] ' + port['name'] + ';\n'
        self.tb_str += '\n' 
        
        self.port_str=''
        for port in self.ports[:-1]:
            self.port_str += ' .' + port['name'] + ' ( ' + port['name'] + ' ),' 
            self.port_str += '\n'
        self.port_str += ' .' + self.ports[-1]['name'] + ' ( ' + self.ports[-1]['name'] + ' )' 
        self.inst_str = ints*'\t' + self.name + ' ' + self.name + '_inst(' 
        self.inst_str += '\n'
        self.inst_str += align.align(self.port_str,tabs,ints+1)
        self.inst_str += '\n'
        self.inst_str += ints*'\t' + ');'
        self.inst_str += '\n'
        self.tb_str += self.inst_str
            
        self.tb_str += '\n' 
        self.tb_str += '\tinitial begin' 
        self.tb_str += '\n' 
        wi=0
        for port in self.ports:
            if port['iodir'] == 'input':
                wi = int(port['datah']) - int(port['datal']) + 1
                self.init_reg += port['name'] + " = " + str(wi) + "'d0;\n"
        self.tb_str += align.align(self.init_reg,tabs,ints+1)
        self.tb_str += '\n' 
        self.tb_str += '\tend' 
        self.tb_str += '\n' 

        self.tb_str += '''
    initial begin
        clk             = 0;
        forever #10 clk = ~clk;
    end

    initial begin
        reset     = 1;
        #15 reset = 0;
        #1000 $finish;
    end

    initial begin
            $fsdbDumpfile("''' + self.name + '''_tb.fsdb");
            $fsdbDumpvars(0,"''' + self.name + '''_tb");
            $fsdbDumpon;
    end

endmodule
'''
        return self.tb_str
