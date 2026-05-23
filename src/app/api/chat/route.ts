// app/api/chat/route.ts
import { NextResponse } from "next/server";
import { Client } from "@gradio/client";

let gradioAppPromise: Promise<any> | null = null;

function getGradioApp() {
  if (!gradioAppPromise) {
    gradioAppPromise = Client.connect("http://localhost:7860");
  }

  return gradioAppPromise;
}

export async function POST(req: Request) {
  try {
    const { message } = await req.json();

    const app = await getGradioApp();

    const result = await app.predict("/stream_response", {
      message: message,
    });

    return NextResponse.json({
      reply: result.data?.[0] ?? result.data,
    });
  } catch (error) {
    console.error("Chat API error:", error);

    return NextResponse.json(
      { error: "Chatbot failed to respond" },
      { status: 500 },
    );
  }
}
