"use client";
import { useState } from "react";
import { Flip, ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const CreateTodo = () => {
  const [task, setTask] = useState("");

  const SubmitHandler = async (e: any) => {
    e.preventDefault(); // Prevent default form submission

    if (!task) {
      toast.error("Add Your Task!", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: 0,
        theme: "colored",
        transition: Flip,
      });
      return; // Early exit to prevent unnecessary API call
    }

    try {
      const res = await fetch("/api/todos", {
        method: "POST",
        body: JSON.stringify({ content: task }),
      });

      if (res.ok) {
        // Handle successful response from the API
        toast.success("Task Added Successfully!", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: 0,
          theme: "colored",
          transition: Flip,
        });
        setTask(""); // Clear the input field after successful creation
      } else {
        toast.error("Failed to Add Task", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: 0,
          theme: "colored",
          transition: Flip,
        });
        console.error("Error adding task:", await res.text());
      }
    } catch (error) {
      toast.error("An error occurred", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: 0,
        theme: "colored",
        transition: Flip,
      });
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <div className="flex flex-col md:flex-row md:gap-5 justify-center items-center gap-2 ">
        <form
          className="flex gap-5 flex-col md:flex-row md:gap-2 items-center justify-center"
          onSubmit={SubmitHandler}
        >
          <input
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Enter Your Task"
            className="w-full flex-wrap text-white bg-slate-900 p-4 rounded-sm focus:border-2 border-solid border-l-blue-500 border-r-cyan-500 border-t-cyan-500 border-b-blue-500 outline-none hover:bg-sky-950 transition duration-300"
          />

          <button className="w-[50%] p-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-md text-md text-white hover:bg-gradient-to-r hover:from-cyan-600 hover:to-blue-800 hover:scale-105 transition duration-300">
            Add Task
          </button>
        </form>
      </div>
      <ToastContainer />
    </div>
  );
};
export default CreateTodo;
