#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.huawei.config import HuaweiInverterSetup


class HuaweiInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, HuaweiInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(HuaweiInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))

    def update(self, inverter_power_reg) -> None:
        power = inverter_power_reg * -1

        _, exported = self.sim_counter.sim_count(power)
        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=HuaweiInverterSetup)
