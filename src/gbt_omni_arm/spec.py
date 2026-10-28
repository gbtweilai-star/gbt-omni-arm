"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "omni_arm",
 "domain": "creation",
 "desc": "Omni-Arm（主人 2026-10-19 六件设计稿的实现版）：**22DoF 手 + 9 骨手臂 + 8 段触手 = 40 骨**，真几何（1080 顶点）/真蒙皮（每顶点权重和=1）/真 GLB，Blender 4.2 本地建件零付费。设计稿归档在 `vendor/omni-arm/source/`；原件**跑不动**（fk 只算 2D、ik 非 CCD、random 决定骨轴 ⇒ 不可复现、生成的 Blender 脚本语法坏、导出路径写死 /mnt/data），本器是**重做后的确定性实现**（零随机：轴/长度/限位全查表）。八条自检：骨 40（skin.joints）/单网格单蒙皮/关节 40/未绑 0/权重归一/顶点>300/尺寸合理/GLB 落盘。op=status/spec/where（纯读）· build（跑 Blender 落件 ⇒ filesystem_write 门在处理器层）。看件页 `holo_pet_w3/omni-arm/index.html`（骨架开关+骨骼树+sha16 自证）",
 "handler": "omni_arm",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "status",
  "spec",
  "where"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
