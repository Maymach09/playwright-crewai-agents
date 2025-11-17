import streamlit as st
import asyncio
from src_full.test_ai_assistant.main import run_agent, run_planner_then_generator, run_full_crew

st.set_page_config(
    page_title="Playwright AI Assistant",
    page_icon="🧠",
    layout="centered",
)

# ---- PAGE HEADER ----
st.markdown(
    """
    <h1 style='text-align: center; font-family: sans-serif;'>🧪 Playwright AI Assistant</h1>
    <p style='text-align: center; color: #666;'>Plan, generate, and heal Playwright tests using CrewAI</p>
    """,
    unsafe_allow_html=True,
)

# ---- SIDEBAR SETTINGS ----
st.sidebar.header("⚙️ Configuration")
agent_name = st.sidebar.selectbox(
    "Select Agent or Full Pipeline",
    [
        "test_planner_agent",
        "test_generator_agent",
        "sequential_workflow",  # NEW: Planner → Generator
        "test_healer_agent",
        "full_crew",
    ],
    help="Choose a specific agent or run workflows",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Planner**: creates test plans\n\n"
    "🧰 **Generator**: writes Playwright scripts (needs test plan)\n\n"
    "🔄 **Sequential Workflow**: runs Planner → Generator\n\n"
    "🩹 **Healer**: debugs & fixes failing tests\n\n"
    "🚀 **Full Crew**: runs all three sequentially"
)

# ---- USER INPUT ----
user_input = st.text_area(
    "💬 Describe what you need:",
    placeholder="e.g., Navigate to Salesforce accounts and create account with minimum data",
    height=120,
)

uploaded_files = st.file_uploader(
    "📎 Upload context files (optional):",
    accept_multiple_files=True,
    type=["txt", "md", "json", "csv", "py", "ts", "js"],
)

# ---- Generator Options ----
if agent_name == "test_generator_agent":
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧰 Generator Options")
    use_latest_plan = st.sidebar.checkbox(
        "Use latest test plan",
        value=True,
        help="Automatically use the most recent test plan as context"
    )
else:
    use_latest_plan = False

# ---- Async execution helper ----
async def run_async_task(func, *args, **kwargs):
    """Run blocking CrewAI calls asynchronously in a thread."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


# ---- Async Full Crew Runner ----
async def run_full_crew_with_progress(user_input, uploaded_files):
    """
    Executes the full multi-agent pipeline (Planner → Generator → Healer)
    with live progress and partial output visualization.
    """
    steps = ["Planner", "Generator", "Healer"]
    status = st.status("🚀 Running Full Crew Pipeline...", expanded=True)

    partial_results = {}
    try:
        for idx, step in enumerate(steps, start=1):
            status.write(f"🔹 Starting **{step}** phase...")
            await asyncio.sleep(0.3)

            if step == "Planner":
                result = await run_async_task(
                    run_agent, "test_planner_agent", user_input, uploaded_files
                )
            elif step == "Generator":
                # Generator uses latest test plan automatically
                result = await run_async_task(
                    run_agent, 
                    "test_generator_agent", 
                    "Generate Playwright tests based on the test plan", 
                    uploaded_files,
                    None,
                    True  # use_latest_test_plan
                )
            else:  # Healer
                result = await run_async_task(
                    run_agent, "test_healer_agent", user_input, uploaded_files
                )

            partial_results[step] = result
            status.write(f"✅ **{step}** completed.")

        status.update(label="✅ Full Crew Pipeline Completed", state="complete", expanded=False)
        return partial_results

    except Exception as e:
        status.update(label=f"❌ Error during full crew run: {e}", state="error", expanded=True)
        return {"error": str(e)}


# ---- Async Sequential Workflow Runner ----
async def run_sequential_workflow_with_progress(user_input):
    """
    Executes Planner → Generator workflow with live progress.
    """
    status = st.status("🔄 Running Sequential Workflow (Planner → Generator)...", expanded=True)

    try:
        # Step 1: Planner
        status.write("🔹 Starting **Planner** phase...")
        await asyncio.sleep(0.3)
        
        planner_result = await run_async_task(
            run_agent, "test_planner_agent", user_input, None
        )
        status.write("✅ **Planner** completed.")
        
        # Step 2: Generator
        status.write("🔹 Starting **Generator** phase...")
        await asyncio.sleep(0.3)
        
        generator_result = await run_async_task(
            run_agent, 
            "test_generator_agent",
            "Generate complete Playwright tests for the scenarios in the test plan",
            None,
            None,
            True  # use_latest_test_plan
        )
        status.write("✅ **Generator** completed.")
        
        status.update(label="✅ Sequential Workflow Completed", state="complete", expanded=False)
        
        return {
            "workflow": "planner_then_generator",
            "Planner": planner_result,
            "Generator": generator_result,
        }

    except Exception as e:
        status.update(label=f"❌ Error during sequential workflow: {e}", state="error", expanded=True)
        return {"error": str(e)}


# ---- RUN BUTTON ----
run_button = st.button("🚀 Run", use_container_width=True)

# ---- MAIN EXECUTION ----
if run_button:
    if not user_input.strip():
        st.warning("⚠️ Please provide a description or scenario.")
    else:
        if agent_name == "sequential_workflow":
            st.info("Running Sequential Workflow: Planner → Generator ⏳")
            
            results = asyncio.run(run_sequential_workflow_with_progress(user_input))
            
            if "error" in results:
                st.error(f"❌ {results['error']}")
            else:
                st.success("✅ Sequential Workflow Completed Successfully!")
                st.subheader("📊 Workflow Results")

                for phase, res in results.items():
                    if phase == "workflow":
                        continue
                    st.markdown(f"### 🔹 {phase} Output")
                    if isinstance(res.get("result"), (dict, list)):
                        st.json(res["result"])
                    else:
                        st.markdown(f"```markdown\n{res.get('result', 'No output')}\n```")

                with st.expander("📄 Full Execution Details"):
                    st.json(results)
        
        elif agent_name == "full_crew":
            st.info("Running full crew asynchronously... this may take a few minutes ⏳")

            results = asyncio.run(run_full_crew_with_progress(user_input, uploaded_files))

            if "error" in results:
                st.error(f"❌ {results['error']}")
            else:
                st.success("✅ Full Crew Completed Successfully!")
                st.subheader("📊 Pipeline Results")

                for phase, res in results.items():
                    st.markdown(f"### 🔹 {phase} Output")
                    if isinstance(res.get("result"), (dict, list)):
                        st.json(res["result"])
                    else:
                        st.markdown(f"```markdown\n{res.get('result', 'No output')}\n```")

                with st.expander("📄 Full Execution Details"):
                    st.json(results)

        else:
            # Single-agent execution
            with st.spinner(f"Running {agent_name}... please wait ⏳"):
                try:
                    # For generator, check if we should use latest test plan
                    if agent_name == "test_generator_agent":
                        result = run_agent(
                            agent_name=agent_name,
                            user_input=user_input,
                            uploaded_files=uploaded_files,
                            use_latest_test_plan=use_latest_plan,
                        )
                    else:
                        result = run_agent(
                            agent_name=agent_name,
                            user_input=user_input,
                            uploaded_files=uploaded_files,
                        )
                    
                    st.success(f"✅ Agent `{agent_name}` completed successfully!")
                    st.subheader("🧠 Output")

                    if isinstance(result.get("result"), (dict, list)):
                        st.json(result["result"])
                    else:
                        st.markdown(f"```markdown\n{result.get('result', 'No output')}\n```")

                    with st.expander("📄 Execution Details"):
                        st.json(result)

                except Exception as e:
                    st.error(f"❌ Error running {agent_name}: {e}")
                    st.exception(e)