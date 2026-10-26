#!/usr/bin/env python3
"""Show safe DTU limits, or update context/output with explicit approval.

No network, model calls, credential output, server changes or global edits.
"""
import argparse
import json
from pathlib import Path
import tempfile
import os

# The published workshop limits (the README table); not a live probe.
SERVER_CONTEXT = {'qwen36': 65536}
SERVER_OUTPUT = {'qwen36': 4096}
CHECKPOINT_CONTEXT = {'qwen36': 262144}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', help='a DTU model id from opencode.json, such as qwen36')
    parser.add_argument('--context', type=int, choices=[4096, 8192, 16384, 32768, 65536, 131072, 262144])
    parser.add_argument('--output', type=int)
    parser.add_argument('--server-max', type=int, help='Organiser-confirmed running server limit, not checkpoint capacity')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    path = root / 'opencode.json'
    if path.is_symlink():
        parser.error('Refusing a symlinked configuration; ask an organiser.')
    original = path.read_bytes()
    try:
        config = json.loads(original)
        models = config['providers']['dtu']['models']
        # Every DTU model in the project configuration that declares limits.
        safe = {name: {k: model['limit'][k] for k in ('context', 'output')}
                for name, model in models.items() if 'limit' in model}
        if any(type(v) is not int or v <= 0 for limits in safe.values() for v in limits.values()):
            raise ValueError('Invalid limits')
    except (ValueError, KeyError, TypeError):
        parser.error('Expected workshop v2 JSON with numeric limits; no changes made. Ask an organiser.')
    if args.context is None and args.output is None:
        print(json.dumps({'kind': 'project_client_budgets',
                          'server_capacity': 'NOT CHECKED: these are not live server limits',
                          'models': safe,
                          'published_limits': {name: {'context': SERVER_CONTEXT[name], 'output': SERVER_OUTPUT[name]}
                                                  for name in safe if name in SERVER_CONTEXT},
                          'no_verified_limit': sorted(name for name in safe if name not in SERVER_CONTEXT)}, indent=2))
        return
    if not args.model:
        parser.error('--model is required for a change')
    if args.model not in safe:
        parser.error(f"Unknown model {args.model!r}; choose one of: {', '.join(sorted(safe))}")
    if args.model not in SERVER_CONTEXT and args.server_max is None:
        parser.error(f'No verified server limit for {args.model}; an organiser must confirm one (--server-max)')
    old = safe[args.model].copy()
    context = args.context if args.context is not None else old['context']
    output = args.output if args.output is not None else old['output']
    ceiling = args.server_max if args.server_max is not None else SERVER_CONTEXT[args.model]
    if ceiling <= 0 or ceiling > CHECKPOINT_CONTEXT.get(args.model, ceiling) or context > ceiling:
        parser.error('Context exceeds the verified server limit; changing client JSON cannot enlarge the server')
    if output < 1 or output > SERVER_OUTPUT.get(args.model, old['output']):
        parser.error('Output exceeds this model gateway cap or is not positive')
    if context <= output:
        parser.error('Context must leave room for input as well as the output allowance')
    if context == old['context'] and output == old['output']:
        print(f'{args.model}: unchanged at {old}')
        return
    config['providers']['dtu']['models'][args.model]['limit'].update(context=context, output=output)
    # Parse again to confirm that this is the sole semantic change.
    checked = json.loads(json.dumps(config))
    checked['providers']['dtu']['models'][args.model]['limit'].update(old)
    if checked != json.loads(original):
        parser.error('Unexpected change; refusing to save')
    if path.read_bytes() != original:
        parser.error('Configuration changed during the check; retry after reviewing it')
    fd, temp_name = tempfile.mkstemp(prefix='.halp-context-', dir=root)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(json.dumps(config, indent=2) + '\n')
        os.chmod(temp_name, path.stat().st_mode & 0o777)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f'{args.model}: {old} -> context {context}, output {output}; all other settings preserved. Run opencode reload, then reopen the project.')


if __name__ == '__main__':
    main()
