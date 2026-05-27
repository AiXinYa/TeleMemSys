#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py - 启动电信运维记忆系统
用法:
  python run.py                    # 默认启动 0.0.0.0:8000
  python run.py --port 8080        # 指定端口
  python run.py --reset            # 重置记忆(清除后重新加载种子数据)
"""

import os, sys, argparse, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")


def main():
    parser = argparse.ArgumentParser(description="电信运维记忆系统")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--reset", action="store_true", help="重置记忆数据")
    args = parser.parse_args()

    sys.path.insert(0, os.path.dirname(__file__))
    data_dir = os.path.join(os.path.dirname(__file__), "data", "memories")

    if args.reset:
        import shutil
        for sub in ["me", "team"]:
            p = os.path.join(data_dir, sub)
            if os.path.exists(p):
                shutil.rmtree(p)
        idx = os.path.join(data_dir, "MEMORY_INDEX.json")
        if os.path.exists(idx):
            os.remove(idx)
        db = os.path.join(data_dir, "..", "sessions.db")
        if os.path.exists(db):
            os.remove(db)
        print("✅ 数据已重置")

    # 加载种子数据
    from src.memory.store import MemoryStore
    from src.memory.types import MemoryEntry, MemoryType, MemoryScope

    store = MemoryStore(data_dir=data_dir)
    if store.stats()["total"] == 0:
        from src.api.seed_data import SEED_MEMORIES
        count = 0
        for item in SEED_MEMORIES:
            try:
                store.save(MemoryEntry(
                    name=item["name"], description=item["description"],
                    type=MemoryType(item["type"]),
                    scope=MemoryScope(item.get("scope", "private")),
                    content=item["content"], tags=item.get("tags", []),
                    why=item.get("why", ""), how_to_apply=item.get("how_to_apply", ""),
                    source="seed",
                ))
                count += 1
            except Exception as e:
                print(f"  ⚠️ {item['name']}: {e}")
        print(f"✅ 已加载 {count} 条种子记忆")
    else:
        stats = store.stats()
        print(f"ℹ️  记忆库: {stats['total']} 条 ({stats['by_dimension']})")

    # 启动服务
    import uvicorn
    print(f"\n🚀 电信运维记忆系统 v0.5.0")
    print(f"   Web UI:  http://{args.host}:{args.port}")
    print(f"   API Doc: http://{args.host}:{args.port}/docs")
    print(f"   数据目录: {data_dir}\n")

    uvicorn.run("src.api.server:app", host=args.host, port=args.port, reload=False, log_level="info")


if __name__ == "__main__":
    main()
