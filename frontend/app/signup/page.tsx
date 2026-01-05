"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { TextField, Button, Typography, Container, Box, Paper, Stack } from "@mui/material";
import { z } from "zod";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";

const schema = z.object({
    email: z.string().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string().min(6),
}).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
});

type SignupFormValues = z.infer<typeof schema>;

export default function SignupPage() {
    const router = useRouter();
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<SignupFormValues>({
        resolver: zodResolver(schema),
    });

    const onSubmit = async (data: SignupFormValues) => {
        try {
            // Adjusted to match common DRF register pattern or user request
            await axios.post("http://localhost:8000/api/accounts/signup/", {
                email: data.email,
                password: data.password,
            });
            alert("Registration success! Please login.");
            router.push("/login");
        } catch (error) {
            console.error(error);
            alert("Signup failed. Check console for details.");
        }
    };

    return (
        <Container maxWidth="xs">
            <Box sx={{ mt: 8, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Paper elevation={3} sx={{ p: 4, width: "100%" }}>
                    <Typography component="h1" variant="h5" textAlign="center" gutterBottom>
                        Create Account
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate sx={{ mt: 1 }}>
                        <Stack spacing={2}>
                            <TextField
                                fullWidth
                                label="Email Address"
                                {...register("email")}
                                error={!!errors.email}
                                helperText={errors.email?.message}
                            />
                            <TextField
                                fullWidth
                                label="Password"
                                type="password"
                                {...register("password")}
                                error={!!errors.password}
                                helperText={errors.password?.message}
                            />
                            <TextField
                                fullWidth
                                label="Confirm Password"
                                type="password"
                                {...register("confirmPassword")}
                                error={!!errors.confirmPassword}
                                helperText={errors.confirmPassword?.message}
                            />
                            <Button type="submit" fullWidth variant="contained" size="large" sx={{ mt: 2 }}>
                                Sign Up
                            </Button>
                            <Typography variant="body2" textAlign="center">
                                Already have an account?{" "}
                                <Link href="/login" style={{ color: "#1976d2", textDecoration: "none" }}>
                                    Login
                                </Link>
                            </Typography>
                        </Stack>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
}
