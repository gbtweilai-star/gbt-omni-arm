# omni_arm

**One capability bit from GBT V8, packaged standalone.** No. 48 of 341,
`creation` domain (Creation).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> Omni-Arm（主人 2026-10-19 六件设计稿的实现版）：**22DoF 手 + 9 骨手臂 + 8 段触手 = 40 骨**，真几何（1080 顶点）/真蒙皮（每顶点权重和=1）/真 GLB，Blender 4.2 本地建件零付费。设计稿归档在 `vendor/omni-arm/source/`；原件**跑不动**（fk 只算 2D、ik 非 CCD、random 决定骨轴 ⇒ 不可复现、生成的 Blender 脚本语法坏、导出路径写死 /mnt/data），本器是**重做后的确定性实现**（零随机：轴/长度/限位全查表）。八条自检：骨 40（skin.joints）/单网格单蒙皮/关节 40/未绑 0/权重归一/顶点>300/尺寸合理/GLB 落盘。op=status/spec/where（纯读）· build（跑 Blender 落件 ⇒ filesystem_write 门在处理器层）。看件页 `holo_pet_w3/omni-arm/index.html`（骨架开关+骨骼树+sha16 自证）

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-omni-arm.git
cd gbt-omni-arm
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_omni_arm info                  # capability card
python -m gbt_omni_arm spec --json           # machine-readable contract
python -m gbt_omni_arm check --payload '{}'
python -m gbt_omni_arm run   --payload '{}'
```

Real `info` output from this machine:

```text
omni_arm  (creation)  v1.0.0
----------------------------------------
Omni-Arm（主人 2026-10-19 六件设计稿的实现版）：**22DoF 手 + 9 骨手臂 + 8 段触手 = 40 骨**，真几何（1080 顶点）/真蒙皮（每顶点权重和=1）/真 GLB，Blender 4.2 本地建件零付费。设计稿归档在 `vendor/omni-arm/source/`；原件**跑不动**（fk 只算 2D、ik 非 CCD、random 决定骨轴 ⇒ 不可复现、生成的 Blender 脚本语法坏、导出路径写死 /mnt/data），本器是**重做后的确定性实现**（零随机：轴/长度/限位全查表）。八条自检：骨 40（skin.joints）/单网格单蒙皮/关节 40/未绑 0/权重归一/顶点>300/尺寸合理/GLB 落盘。op=status/spec/where（纯读）· build（跑 Blender 落件 ⇒ filesystem_write 门在处理器层）。看件页 `holo_pet_w3/omni-arm/index.html`（骨架开关+骨骼树+sha16 自证）

gated      : True   <- needs explicit consent
external   : False
multi-op   : True
params     : (none)
values     : status, spec, where
```

Wire a real implementation:

```python
from gbt_omni_arm import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（3 个）**：`status`、`spec`、`where`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `omni_arm` |
| domain | `creation` |
| handler | `omni_arm` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [creation/omni_arm](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/creation/omni_arm.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
