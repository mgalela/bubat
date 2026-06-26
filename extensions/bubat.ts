import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

type Route = {
  pattern: RegExp;
  skill: string;
  argFrom?: number;
};

const routes: Route[] = [
  { pattern: /^stage\s+(.+)$/i, skill: "bubat-stage", argFrom: 1 },
  { pattern: /^raw\s+add\s+(.+)$/i, skill: "bubat-raw-add", argFrom: 1 },
  { pattern: /^raw\s+route$/i, skill: "bubat-raw-route" },
  { pattern: /^refresh\s+index$/i, skill: "bubat-refresh-index" },
  { pattern: /^sync\s+index\s+(.+)$/i, skill: "bubat-sync-index", argFrom: 1 },
  { pattern: /^diagram\s+(.+)$/i, skill: "bubat-diagram", argFrom: 1 },
  { pattern: /^update\s+(.+)$/i, skill: "bubat-update", argFrom: 1 },
  { pattern: /^triage\s+(.+)$/i, skill: "bubat-triage", argFrom: 1 },
  { pattern: /^bridge$/i, skill: "bubat-bridge" },
  { pattern: /^sync\s+graphify$/i, skill: "bubat-graphify-sync" },
  { pattern: /^(?:where|trace|find\s+artifact)\s+(.+)$/i, skill: "bubat-trace", argFrom: 1 },
  { pattern: /^status$/i, skill: "bubat-status" },
];

function toSkillCommand(skill: string, arg?: string): string {
  return arg?.trim() ? `/skill:${skill} ${arg.trim()}` : `/skill:${skill}`;
}

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    if (ctx.hasUI) ctx.ui.setStatus("bubat", "BUBAT ready");
  });

  pi.on("input", async (event) => {
    const text = event.text.trim();

    if (/^setup$/i.test(text)) {
      return {
        action: "transform" as const,
        text: "Run BUBAT onboarding setup. Resolve workspace root, read setup/questionnaire.md, then populate shared/system-meta.md.",
      };
    }

    for (const route of routes) {
      const match = text.match(route.pattern);
      if (!match) continue;

      return {
        action: "transform" as const,
        text: toSkillCommand(route.skill, route.argFrom ? match[route.argFrom] : undefined),
      };
    }

    return { action: "continue" as const };
  });
}
