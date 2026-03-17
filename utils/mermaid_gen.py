"""
Mermaid diagram generator for KadiRail legal case maps.
"""

from typing import List, Optional
from core.map_engine import KadiRailMap, LegalStep


def generate_case_map_mermaid(map_obj: KadiRailMap) -> str:
    """
    Generate Mermaid flowchart code from a KadiRailMap.

    Args:
        map_obj: KadiRailMap instance

    Returns:
        Mermaid flowchart markdown string
    """
    lines = ["flowchart TD"]

    # Add styling
    lines.append("    classDef default fill:#f9fafb,stroke:#374151,stroke-width:1px")
    lines.append(
        "    classDef current fill:#4F46E5,stroke:#3730a3,stroke-width:2px,color:#fff"
    )
    lines.append(
        "    classDef completed fill:#10B981,stroke:#047857,stroke-width:2px,color:#fff"
    )
    lines.append("    classDef optional fill:#F59E0B,stroke:#B45309,stroke-width:1px")
    lines.append("    classDef parallel fill:#8B5CF6,stroke:#6D28D9,stroke-width:1px")

    # Track connections
    step_ids = []

    for i, step in enumerate(map_obj.steps):
        # Create node ID
        node_id = f"step{i + 1}"
        step_ids.append(node_id)

        # Node label
        label = f"**{step.title}**<br/>({step.duration_days} วัน)"

        # Add node
        lines.append(f'    {node_id}["{label}"]')

        # Apply styling based on state
        if i < map_obj.current_step:
            lines.append(f"    class {node_id} completed")
        elif i == map_obj.current_step:
            lines.append(f"    class {node_id} current")
        elif step.optional:
            lines.append(f"    class {node_id} optional")
        elif step.parallel:
            lines.append(f"    class {node_id} parallel")

        # Add description as tooltip
        desc_escaped = step.description.replace('"', "'").replace("\n", " ")
        lines.append(f'    click {node_id} "{desc_escaped}"')

    # Add connections between steps
    for i in range(len(step_ids) - 1):
        lines.append(f"    {step_ids[i]} --> {step_ids[i + 1]}")

    # Add alternative paths if any
    for i, step in enumerate(map_obj.steps):
        if step.alternatives and i > 0:
            for alt_idx, alt in enumerate(
                step.alternatives[:2]
            ):  # Limit to 2 alternatives
                alt_node = f"alt{i + 1}_{alt_idx + 1}"
                alt_label = f"*{alt}*"
                lines.append(f'    {alt_node}["{alt_label}"]')
                lines.append(f"    {step_ids[max(0, i - 1)]} -.-> {alt_node}")
                lines.append(f"    class {alt_node} optional")

    return "\n".join(lines)


def generate_timeline_mermaid(steps: List[LegalStep], current_step: int = 0) -> str:
    """
    Generate a timeline/sequence diagram.

    Args:
        steps: List of LegalStep
        current_step: Current step index

    Returns:
        Mermaid timeline markdown
    """
    lines = ["timeline"]
    lines.append(f"    title Timeline: {len(steps)} Steps")

    for i, step in enumerate(steps):
        marker = "✅" if i < current_step else ("🔄" if i == current_step else "⏳")
        lines.append(f"        {marker} {step.title} : {step.duration_days} days")

    return "\n".join(lines)


def generate_gantt_mermaid(steps: List[LegalStep]) -> str:
    """
    Generate a Gantt chart.

    Args:
        steps: List of LegalStep

    Returns:
        Mermaid Gantt markdown
    """
    lines = ["gantt"]
    lines.append("    title Legal Case Timeline")
    lines.append("    dateFormat  YYYY-MM-DD")
    lines.append("    axisFormat  %d %b")

    # Calculate dates
    from datetime import datetime, timedelta

    start_date = datetime.now()

    for i, step in enumerate(steps):
        task_id = f"task{i + 1}"
        start_offset = sum(s.duration_days for s in steps[:i])
        duration = step.duration_days

        lines.append(f"    {step.title} : {task_id}, {start_offset}, {duration}d")

    return "\n".join(lines)


def generate_flowchart_mermaid(
    title: str, nodes: List[dict], connections: List[tuple]
) -> str:
    """
    Generic flowchart generator.

    Args:
        title: Flowchart title
        nodes: List of dicts with 'id', 'label', 'style'
        connections: List of tuples (from_id, to_id, label)

    Returns:
        Mermaid flowchart markdown
    """
    lines = ["flowchart LR"]
    lines.append(f"    title {title}")

    # Add nodes
    for node in nodes:
        node_id = node.get("id", "")
        label = node.get("label", node_id)
        style = node.get("style", "")

        if style:
            lines.append(f'    {node_id}["{label}"] ::: {style}')
        else:
            lines.append(f'    {node_id}["{label}"]')

    # Add connections
    for conn in connections:
        from_id, to_id = conn[0], conn[1]
        label = conn[2] if len(conn) > 2 else ""

        if label:
            lines.append(f"    {from_id} -->|{label}| {to_id}")
        else:
            lines.append(f"    {from_id} --> {to_id}")

    return "\n".join(lines)


def render_mermaid_inline(mermaid_code: str, height: int = 400) -> str:
    """
    Wrap Mermaid code in HTML for inline rendering.

    Args:
        mermaid_code: Mermaid diagram code
        height: Height in pixels

    Returns:
        HTML string
    """
    return f"""
    <div class="mermaid" style="text-align: center;">
    {mermaid_code}
    </div>
    """


def generate_comparison_chart(options: List[dict]) -> str:
    """
    Generate a comparison chart for What-If Simulator.

    Args:
        options: List of option dicts with 'name', 'cost', 'time', 'success_rate'

    Returns:
        Mermaid flowchart comparing options
    """
    lines = ["flowchart TB"]
    lines.append("    subgraph Options")

    for i, opt in enumerate(options):
        opt_id = f"opt{i + 1}"
        lines.append(f"    {opt_id}[{opt['name']}]")

    lines.append("    end")

    # Add decision logic
    lines.append("    start{START} --> Options")

    for i, opt in enumerate(options):
        opt_id = f"opt{i + 1}"
        # Calculate success/fail branches
        success = int(opt.get("success_rate", 50))

        lines.append(f"    {opt_id} -->|ชนะ {success}%| success{i + 1}(ชนะคดี)")
        lines.append(f"    {opt_id} -->|แพ้ {100 - success}%| fail{i + 1}(แพ้คดี)")

    return "\n".join(lines)
