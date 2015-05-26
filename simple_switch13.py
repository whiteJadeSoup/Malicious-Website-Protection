
# coding=utf-8
from __future__ import division



from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER,HANDSHAKE_DISPATCHER,DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3


from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import udp
from ryu.lib.packet import tcp
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu.lib.packet import icmp
from ryu.lib.packet import arp
from ryu.lib import hub


import random
import math
import time
import thread

from Levenshtein import *

import resolve
import db



class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        db.importMysql()





    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        match = parser.OFPMatch()
        self.add_flow(datapath, 0, match, actions,idle_timeout=0,hard_timeout=0)




    '''
    方法说明：添加流表
    方法参数：datapath--交换机
              priority--流表优先级
              match--流表匹配信息
              actions--流表执行的行动
              buffer_id--数据包在交换机缓存区的ID
              idle_timeout--最大活跃时间
              hard_timeout--最大生存时间
    '''
    def add_flow(self, datapath, priority, match, actions, 
                 buffer_id=None, idle_timeout=0, hard_timeout=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
            
            
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst,idle_timeout=idle_timeout,
                                    hard_timeout=hard_timeout,flags=ofproto.OFPFF_SEND_FLOW_REM)
            
            
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst,
                                    idle_timeout=idle_timeout,
                                    hard_timeout=hard_timeout,flags=ofproto.OFPFF_SEND_FLOW_REM)
                
        datapath.send_msg(mod)





    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                ev.msg.msg_len, ev.msg.total_len)


        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        try:
            pkt = packet.Packet(msg.data)
        except:
            return 


        pkt_eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst = pkt_eth.dst
        src = pkt_eth.src

        self.logger.info("packet in dpid=%s %s %s in_port=%s", dpid, src, dst, in_port)


        queriy_name = ''

        pkt_udp = pkt.get_protocol(udp.udp)
        if pkt_udp:

            if pkt_udp.dst_port==53 or pkt_udp.src_port == 53:
                print 'DNS request'

                #获取DNS请求内容
                queriy_content = [p for p in pkt.protocols if type(p) == str]
            
                #test
                with open("dns","w") as f:
                    f.write(queriy_content[0])
                    
                queriy_name = resolve.getHostName(queriy_content[0]).replace('www.','')


                print '域名：' + queriy_name
                #不是白名单？
                if db.iswhite_list(queriy_name) == 0:

                    #黑名单？
                    if db.isblack_list(queriy_name):
                        print '黑名单: ' + queriy_name
                        return

                    else:
                        #编辑距离在[1:2]?
                        white_lists = db.getWhite_list()

                        for list in white_lists:
                            edit_dis = distance(queriy_name,list)
                            if edit_dis >= 1 and edit_dis <= 2:
                                print '可疑域名：' + queriy_name

                                return
                            
                            
                print '白名单: ' + queriy_name
        # 学习mac地址防止下次再次flood.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD



        actions = [parser.OFPActionOutput(out_port)]


        # 添加一条流表项
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(eth_src=src, eth_dst=dst)
            

            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id,5,5)

            else:
                self.add_flow(datapath, 1, match, actions,idle_timeout=5,hard_timeout=5)



        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)



