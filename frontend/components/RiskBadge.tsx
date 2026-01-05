import { Chip } from "@mui/material";

interface RiskBadgeProps {
    level: "LOW" | "MEDIUM" | "HIGH";
}

export default function RiskBadge({ level }: RiskBadgeProps) {
    const colors: Record<string, "success" | "warning" | "error"> = {
        LOW: "success",
        MEDIUM: "warning",
        HIGH: "error",
    };

    return (
        <Chip
            label={`${level} RISK`}
            color={colors[level] || "default"}
            sx={{ fontWeight: "bold", fontSize: "1rem", px: 2, py: 2 }}
        />
    );
}
