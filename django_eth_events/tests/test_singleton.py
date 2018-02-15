# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from eth_tester import EthereumTester
from web3 import RPCProvider, IPCProvider
from web3.providers.eth_tester import EthereumTesterProvider
from django_eth_events.web3_service import Web3Service
from django_eth_events.event_listener import EventListener


class TestSingleton(TestCase):

    def test_single_instance(self):
        service1 = Web3Service()
        service2 = Web3Service()
        self.assertEqual(service1.web3, service2.web3)

    def test_arg_rpc_provider(self):
        rpc_provider = RPCProvider(
            host='localhost',
            port=8545,
            ssl=0
        )

        service1 = Web3Service()
        service2 = Web3Service(rpc_provider)
        self.assertEqual(service1.web3, service2.web3)

    def test_arg_ipc_provider(self):
        ipc_provider = IPCProvider(
            ipc_path='',
            testnet=True
        )

        service1 = Web3Service()
        self.assertIsInstance(service1.web3.providers[0], RPCProvider)
        service2 = Web3Service(ipc_provider)
        self.assertIsInstance(service2.web3.providers[0], IPCProvider)
        self.assertEqual(service2.web3.providers[0], ipc_provider)

    def test_eth_tester_provider(self):
        eth_tester_provider = EthereumTesterProvider(EthereumTester())

        service1 = Web3Service()
        self.assertIsInstance(service1.web3.providers[0], RPCProvider)
        service2 = Web3Service(eth_tester_provider)
        self.assertIsInstance(service2.web3.providers[0], EthereumTesterProvider)
        self.assertEqual(service2.web3.providers[0], eth_tester_provider)

    def test_event_listener_singleton(self):
        ipc_provider = IPCProvider(
            ipc_path='',
            testnet=True
        )

        listener1 = EventListener()
        listener2 = EventListener()
        self.assertEqual(listener1, listener2)
        listener3 = EventListener(provider=ipc_provider)
        self.assertNotEqual(listener2, listener3)
